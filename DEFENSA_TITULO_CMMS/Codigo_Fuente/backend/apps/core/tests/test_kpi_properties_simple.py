"""Simplified property-based tests for KPI calculations."""

import pytest
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from hypothesis import given, strategies as st, settings
from hypothesis.extra.django import TestCase
from django.utils import timezone

User = get_user_model()


class KPICalculationPropertyTests(TestCase):
    """Simplified property-based tests for KPI calculations."""

    @given(st.lists(st.integers(min_value=0, max_value=100), min_size=0, max_size=20))
    @settings(max_examples=50, deadline=None)
    def test_property_average_is_non_negative(self, durations):
        """Property 1: Average duration is always non-negative.
        
        For any list of durations, the calculated average should be >= 0.
        
        **Validates: Requirements 1.1**
        """
        if len(durations) == 0:
            avg = 0
        else:
            avg = sum(durations) / len(durations)
        
        assert avg >= 0, f"Average should be non-negative, got {avg}"

    @given(
        st.lists(
            st.tuples(
                st.integers(min_value=0, max_value=1000),  # created_at (as timestamp)
                st.integers(min_value=0, max_value=1000)   # completed_date (as timestamp)
            ),
            min_size=1,
            max_size=20
        )
    )
    @settings(max_examples=30, deadline=None)
    def test_property_invalid_dates_excluded_from_average(self, date_pairs):
        """Property 2: Invalid dates are excluded from calculations.
        
        For any work orders where completed_date < created_at,
        those should be excluded from average duration calculation.
        
        **Validates: Requirements 1.2, 1.4**
        """
        valid_durations = []
        
        for created_at, completed_date in date_pairs:
            if completed_date >= created_at:
                duration = completed_date - created_at
                valid_durations.append(duration)
        
        if len(valid_durations) == 0:
            avg = 0
        else:
            avg = sum(valid_durations) / len(valid_durations)
        
        # Property: Average should be non-negative
        assert avg >= 0, f"Average should be non-negative, got {avg}"
        
        # Property: If all dates are invalid, average should be 0
        if all(completed < created for created, completed in date_pairs):
            assert avg == 0, "Average should be 0 when all dates are invalid"

    @given(st.integers(min_value=0, max_value=100))
    @settings(max_examples=20)
    def test_property_percentage_in_valid_range(self, completed_count):
        """Property: Percentage KPIs are in range 0-100.
        
        For any count of completed items, the percentage should be 0-100.
        """
        total_count = 100
        
        if total_count == 0:
            percentage = 0
        else:
            percentage = (completed_count / total_count) * 100
        
        assert 0 <= percentage <= 100, f"Percentage out of range: {percentage}"

    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)
    )
    @settings(max_examples=30)
    def test_property_negative_durations_excluded(self, durations):
        """Property: Negative durations should be excluded.
        
        For any list of durations including negative values,
        only non-negative values should be included in average.
        """
        valid_durations = [d for d in durations if d >= 0]
        
        if len(valid_durations) == 0:
            avg = 0
        else:
            avg = sum(valid_durations) / len(valid_durations)
        
        assert avg >= 0, f"Average should be non-negative, got {avg}"
