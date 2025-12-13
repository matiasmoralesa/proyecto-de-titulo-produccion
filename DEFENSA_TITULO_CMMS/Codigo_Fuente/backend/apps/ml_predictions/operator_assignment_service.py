"""
Operator Assignment Service
Assigns the most qualified and available operator to work orders based on skills and availability.
"""
from django.db.models import Q, F, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import logging

from apps.authentication.models import User
from apps.ml_predictions.models import (
    OperatorSkill,
    OperatorAvailability,
    OperatorPerformance
)
from apps.work_orders.models import WorkOrder

logger = logging.getLogger(__name__)


class OperatorAssignmentService:
    """
    Service for intelligent operator assignment based on:
    - Skills and certifications
    - Current availability
    - Performance history
    - Location proximity
    - Workload balance
    """
    
    def __init__(self):
        self.skill_weight = 0.35
        self.availability_weight = 0.25
        self.performance_weight = 0.25
        self.location_weight = 0.15
    
    def find_best_operator(
        self,
        work_order: WorkOrder,
        required_skills: Optional[List[str]] = None,
        min_proficiency: int = 3
    ) -> Optional[User]:
        """
        Find the best operator for a work order.
        
        Args:
            work_order: The work order to assign
            required_skills: List of required skill names
            min_proficiency: Minimum proficiency level (1-5)
        
        Returns:
            User object of the best operator, or None if no suitable operator found
        """
        from apps.authentication.models import Role
        
        # Get all operators (users with OPERADOR role only)
        operators = User.objects.filter(
            role__name=Role.OPERADOR,
            is_active=True
        )
        
        if not operators.exists():
            logger.warning("No operators found in the system")
            return None
        
        # Score each operator
        operator_scores = []
        
        for operator in operators:
            score = self._calculate_operator_score(
                operator,
                work_order,
                required_skills,
                min_proficiency
            )
            
            if score > 0:  # Only consider operators with positive scores
                operator_scores.append({
                    'operator': operator,
                    'score': score,
                    'details': self._get_score_details(operator, work_order)
                })
        
        if not operator_scores:
            logger.warning(f"No suitable operators found for work order {work_order.id}")
            return None
        
        # Sort by score (highest first)
        operator_scores.sort(key=lambda x: x['score'], reverse=True)
        
        best_match = operator_scores[0]
        logger.info(
            f"Best operator for WO {work_order.id}: {best_match['operator'].get_full_name()} "
            f"(score: {best_match['score']:.2f})"
        )
        
        return best_match['operator']
    
    def _calculate_operator_score(
        self,
        operator: User,
        work_order: WorkOrder,
        required_skills: Optional[List[str]],
        min_proficiency: int
    ) -> float:
        """Calculate overall score for an operator."""
        
        # 1. Skills score
        skills_score = self._calculate_skills_score(
            operator,
            work_order,
            required_skills,
            min_proficiency
        )
        
        if skills_score == 0:
            return 0  # Operator doesn't meet minimum requirements
        
        # 2. Availability score
        availability_score = self._calculate_availability_score(operator)
        
        # 3. Performance score
        performance_score = self._calculate_performance_score(operator)
        
        # 4. Location score
        location_score = self._calculate_location_score(operator, work_order)
        
        # Calculate weighted total
        total_score = (
            skills_score * self.skill_weight +
            availability_score * self.availability_weight +
            performance_score * self.performance_weight +
            location_score * self.location_weight
        )
        
        return total_score
    
    def _calculate_skills_score(
        self,
        operator: User,
        work_order: WorkOrder,
        required_skills: Optional[List[str]],
        min_proficiency: int
    ) -> float:
        """Calculate skills match score (0-100)."""
        
        # Get operator skills
        operator_skills = OperatorSkill.objects.filter(operator=operator)
        
        if not operator_skills.exists():
            return 0
        
        # Check vehicle type skill
        vehicle_type_skill = operator_skills.filter(
            skill_category='VEHICLE_TYPE',
            skill_name=work_order.asset.vehicle_type,
            proficiency_level__gte=min_proficiency
        ).first()
        
        if not vehicle_type_skill:
            return 0  # Must have vehicle type skill
        
        score = vehicle_type_skill.proficiency_level * 10  # Base score from vehicle skill
        
        # Check additional required skills
        if required_skills:
            matched_skills = 0
            total_proficiency = 0
            
            for skill_name in required_skills:
                skill = operator_skills.filter(
                    skill_name=skill_name,
                    proficiency_level__gte=min_proficiency
                ).first()
                
                if skill:
                    matched_skills += 1
                    total_proficiency += skill.proficiency_level
            
            if matched_skills > 0:
                skill_match_ratio = matched_skills / len(required_skills)
                avg_proficiency = total_proficiency / matched_skills
                score += (skill_match_ratio * avg_proficiency * 20)
        
        # Bonus for certifications
        certified_skills = operator_skills.filter(is_certified=True).count()
        score += min(certified_skills * 5, 20)  # Max 20 bonus points
        
        return min(score, 100)
    
    def _calculate_availability_score(self, operator: User) -> float:
        """Calculate availability score (0-100)."""
        
        try:
            availability = OperatorAvailability.objects.get(operator=operator)
        except OperatorAvailability.DoesNotExist:
            # Create default availability
            availability = OperatorAvailability.objects.create(
                operator=operator,
                is_available=True
            )
        
        if not availability.is_available:
            return 0
        
        # Check if within shift hours
        now = timezone.now().time()
        if availability.shift_start and availability.shift_end:
            if not (availability.shift_start <= now <= availability.shift_end):
                return 30  # Reduced score if outside shift
        
        # Score based on current workload
        workload_score = 100
        
        if availability.active_work_orders > 0:
            # Reduce score based on number of active work orders
            workload_penalty = min(availability.active_work_orders * 15, 60)
            workload_score -= workload_penalty
        
        if availability.estimated_hours_remaining > 0:
            # Reduce score based on estimated hours
            hours_penalty = min(availability.estimated_hours_remaining * 5, 30)
            workload_score -= hours_penalty
        
        return max(workload_score, 10)  # Minimum 10 if available
    
    def _calculate_performance_score(self, operator: User) -> float:
        """Calculate performance score (0-100)."""
        
        # Get recent performance (last 90 days)
        ninety_days_ago = timezone.now().date() - timedelta(days=90)
        
        recent_performance = OperatorPerformance.objects.filter(
            operator=operator,
            period_end__gte=ninety_days_ago
        ).aggregate(
            avg_score=Avg('performance_score'),
            avg_success_rate=Avg('success_rate')
        )
        
        if recent_performance['avg_score']:
            return recent_performance['avg_score']
        
        # If no performance data, check skills success rate
        skills = OperatorSkill.objects.filter(operator=operator)
        if skills.exists():
            avg_success_rate = skills.aggregate(avg=Avg('success_rate'))['avg']
            return avg_success_rate if avg_success_rate else 75
        
        return 75  # Default score for new operators
    
    def _calculate_location_score(self, operator: User, work_order: WorkOrder) -> float:
        """Calculate location proximity score (0-100)."""
        
        try:
            availability = OperatorAvailability.objects.get(operator=operator)
            
            if availability.current_location and work_order.asset.location:
                # If same location, perfect score
                if availability.current_location == work_order.asset.location:
                    return 100
                
                # If different location, reduced score
                return 50
            
        except OperatorAvailability.DoesNotExist:
            pass
        
        return 70  # Default score if location unknown
    
    def _get_score_details(self, operator: User, work_order: WorkOrder) -> Dict:
        """Get detailed scoring breakdown for logging/debugging."""
        
        return {
            'operator_name': operator.get_full_name(),
            'skills': self._calculate_skills_score(operator, work_order, None, 3),
            'availability': self._calculate_availability_score(operator),
            'performance': self._calculate_performance_score(operator),
            'location': self._calculate_location_score(operator, work_order)
        }
    
    def assign_operator_to_work_order(
        self,
        work_order: WorkOrder,
        required_skills: Optional[List[str]] = None,
        auto_assign: bool = True
    ) -> Optional[User]:
        """
        Find and assign the best operator to a work order.
        
        Args:
            work_order: The work order to assign
            required_skills: List of required skill names
            auto_assign: If True, automatically assign the operator to the work order
        
        Returns:
            Assigned operator or None
        """
        
        best_operator = self.find_best_operator(work_order, required_skills)
        
        if best_operator and auto_assign:
            work_order.assigned_to = best_operator
            work_order.save()
            
            # Update operator availability
            availability, created = OperatorAvailability.objects.get_or_create(
                operator=best_operator
            )
            availability.active_work_orders = F('active_work_orders') + 1
            availability.save()
            
            logger.info(
                f"Assigned work order {work_order.id} to {best_operator.get_full_name()}"
            )
        
        return best_operator
    
    def update_operator_workload(self, operator: User):
        """Update operator's current workload based on active work orders."""
        
        active_work_orders = WorkOrder.objects.filter(
            assigned_to=operator,
            status__in=['pending', 'in_progress']
        )
        
        total_hours = sum(
            wo.estimated_hours or 0 for wo in active_work_orders
        )
        
        availability, created = OperatorAvailability.objects.get_or_create(
            operator=operator
        )
        
        availability.active_work_orders = active_work_orders.count()
        availability.estimated_hours_remaining = total_hours
        availability.save()
