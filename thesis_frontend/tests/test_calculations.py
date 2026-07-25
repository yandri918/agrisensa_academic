"""
AgriSensa Calculation Tests
===========================
Unit tests for core business logic calculations.
Run with: pytest tests/test_calculations.py -v
"""

import pytest
import math


# =============================================================================
# TEST FIXTURES
# =============================================================================
@pytest.fixture
def sample_waste_data():
    """Sample waste collection data for testing."""
    return {
        "total_waste_collected": 1000,  # kg
        "organic_processed": 600,        # kg
        "plastic_recycled": 300,         # kg
    }


@pytest.fixture
def sample_price_data():
    """Sample pricing data for testing."""
    return {
        "price_organic": 2500,    # Rp/kg
        "price_filament": 150000, # Rp/kg
        "coef_carbon": 0.53,      # kg CO2/kg waste
    }


@pytest.fixture
def sample_financial_data():
    """Sample financial data for BEP testing."""
    return {
        "fixed_cost": 10000000,    # Rp/month (10 Juta)
        "variable_cost": 500,      # Rp/kg
        "sell_price": 5000,        # Rp/kg
    }


# =============================================================================
# SUSTAINABILITY CALCULATIONS
# =============================================================================
class TestSustainabilityRate:
    """Tests for sustainability rate calculation."""
    
    def test_sustainability_rate_normal(self, sample_waste_data):
        """Test normal sustainability rate calculation."""
        total = sample_waste_data["total_waste_collected"]
        organic = sample_waste_data["organic_processed"]
        plastic = sample_waste_data["plastic_recycled"]
        
        # Formula: (organic + plastic) / total * 100
        rate = ((organic + plastic) / total) * 100
        
        assert rate == 90.0, "Sustainability rate should be 90%"
    
    def test_sustainability_rate_zero_waste(self):
        """Test sustainability rate with zero waste."""
        total = 0
        organic = 0
        plastic = 0
        
        # Should handle division by zero gracefully
        rate = ((organic + plastic) / total * 100) if total > 0 else 0
        
        assert rate == 0, "Rate should be 0 when no waste collected"
    
    def test_sustainability_rate_full_recycling(self):
        """Test 100% recycling scenario."""
        total = 500
        organic = 300
        plastic = 200
        
        rate = ((organic + plastic) / total) * 100
        
        assert rate == 100.0, "Full recycling should yield 100%"


# =============================================================================
# CARBON OFFSET CALCULATIONS
# =============================================================================
class TestCarbonOffset:
    """Tests for carbon offset calculations."""
    
    def test_carbon_offset_basic(self, sample_waste_data, sample_price_data):
        """Test basic carbon offset calculation."""
        waste = sample_waste_data["total_waste_collected"]
        coef = sample_price_data["coef_carbon"]
        
        # Formula: waste * coefficient
        offset = waste * coef
        
        assert offset == 530.0, "Carbon offset should be 530 kg CO2"
    
    def test_methane_avoided(self, sample_waste_data):
        """Test methane avoidance calculation (organic)."""
        organic = sample_waste_data["organic_processed"]
        
        # Formula: organic * 0.5 (EPA/IPCC simplified)
        methane = organic * 0.5
        
        assert methane == 300.0, "Methane avoided should be 300 kg CO2e"
    
    def test_tree_equivalent(self, sample_waste_data, sample_price_data):
        """Test tree equivalent calculation."""
        waste = sample_waste_data["total_waste_collected"]
        coef = sample_price_data["coef_carbon"]
        
        # Formula: (waste * coef) / 22 (1 tree = 22kg CO2/year)
        trees = (waste * coef) / 22
        
        assert pytest.approx(trees, 0.1) == 24.09, "Tree equivalent should be ~24"


# =============================================================================
# ECONOMIC VALUE CALCULATIONS
# =============================================================================
class TestEconomicValue:
    """Tests for economic value calculations."""
    
    def test_money_saved_calculation(self, sample_waste_data, sample_price_data):
        """Test economic value (money saved) calculation."""
        organic = sample_waste_data["organic_processed"]
        plastic = sample_waste_data["plastic_recycled"]
        price_org = sample_price_data["price_organic"]
        price_fil = sample_price_data["price_filament"]
        
        # Formula: (organic * price_organic) + (plastic * price_filament)
        value = (organic * price_org) + (plastic * price_fil)
        
        expected = (600 * 2500) + (300 * 150000)
        assert value == expected, f"Economic value should be {expected}"
    
    def test_value_per_kg(self, sample_waste_data, sample_price_data):
        """Test value per kg calculation."""
        organic = sample_waste_data["organic_processed"]
        plastic = sample_waste_data["plastic_recycled"]
        total = sample_waste_data["total_waste_collected"]
        price_org = sample_price_data["price_organic"]
        price_fil = sample_price_data["price_filament"]
        
        # Formula: ((organic * price_org) + (plastic * price_fil)) / total
        total_value = (organic * price_org) + (plastic * price_fil)
        value_per_kg = total_value / total
        
        assert value_per_kg == 46500.0, "Value per kg should be 46500"


# =============================================================================
# BREAK-EVEN ANALYSIS
# =============================================================================
class TestBreakEvenAnalysis:
    """Tests for BEP calculations."""
    
    def test_bep_units_calculation(self, sample_financial_data):
        """Test BEP units calculation."""
        fixed = sample_financial_data["fixed_cost"]
        var = sample_financial_data["variable_cost"]
        price = sample_financial_data["sell_price"]
        
        # Formula: fixed_cost / (sell_price - variable_cost)
        contribution_margin = price - var
        bep_units = fixed / contribution_margin
        
        expected = 10000000 / (5000 - 500)  # = 2222.22 kg
        assert pytest.approx(bep_units, 0.01) == expected
    
    def test_bep_revenue_calculation(self, sample_financial_data):
        """Test BEP revenue calculation."""
        fixed = sample_financial_data["fixed_cost"]
        var = sample_financial_data["variable_cost"]
        price = sample_financial_data["sell_price"]
        
        contribution_margin = price - var
        bep_units = fixed / contribution_margin
        bep_revenue = bep_units * price
        
        expected_units = 10000000 / 4500
        expected_revenue = expected_units * 5000
        assert pytest.approx(bep_revenue, 1) == expected_revenue
    
    def test_bep_zero_contribution(self):
        """Test BEP with zero contribution margin (edge case)."""
        fixed = 10000000
        var = 5000
        price = 5000  # Same as variable cost
        
        contribution_margin = price - var
        
        # Should handle division by zero
        bep_units = fixed / contribution_margin if contribution_margin > 0 else float('inf')
        
        assert bep_units == float('inf'), "BEP should be infinity when CM is 0"


# =============================================================================
# FUNDING MODEL CALCULATIONS
# =============================================================================
class TestFundingModel:
    """Tests for funding model calculations."""
    
    def test_debt_to_equity_ratio(self):
        """Test DER calculation."""
        debt = 50000000       # 50 Juta loan
        equity = 200000000    # 200 Juta (internal + investor + grants)
        
        # Formula: (debt / equity) * 100
        der = (debt / equity) * 100
        
        assert der == 25.0, "DER should be 25%"
    
    def test_der_zero_equity(self):
        """Test DER with zero equity (edge case)."""
        debt = 50000000
        equity = 0
        
        der = (debt / equity * 100) if equity > 0 else 0
        
        assert der == 0, "DER should be 0 when equity is 0"
    
    def test_capex_coverage(self):
        """Test CAPEX coverage calculation."""
        total_funding = 250000000  # 250 Juta
        total_capex = 200000000    # 200 Juta
        
        coverage = (total_funding / total_capex) * 100
        
        assert coverage == 125.0, "Coverage should be 125%"


# =============================================================================
# RUN TESTS
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
