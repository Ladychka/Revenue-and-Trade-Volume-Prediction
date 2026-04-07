from enum import Enum
from decimal import Decimal, ROUND_HALF_UP

class ExciseCategory(str, Enum):
    ALCOHOL = "ALCOHOL"
    TOBACCO = "TOBACCO"
    FUEL = "FUEL"
    VEHICLES = "VEHICLES"
    LUXURY_GOODS = "LUXURY_GOODS"
    EXEMPT = "EXEMPT"

class ExciseCalculator:
    """
    Solves the V1 Excise Tax Gap ("Always returns 0").
    Provides deterministic, rule-based excise tax logic for analytics.
    """

    # Baseline statutory equivalent rates for scenario simulation
    DEFAULT_RATES = {
        ExciseCategory.ALCOHOL: Decimal("0.35"),       # 35% Ad Valorem
        ExciseCategory.TOBACCO: Decimal("0.40"),       # 40% Ad Valorem
        ExciseCategory.FUEL: Decimal("0.25"),          # 25% Ad Valorem equivalent
        ExciseCategory.VEHICLES: Decimal("0.10"),      # 10% Ad Valorem
        ExciseCategory.LUXURY_GOODS: Decimal("0.20"),  # 20% Ad Valorem
        ExciseCategory.EXEMPT: Decimal("0.00"),
    }

    @classmethod
    def calculate_excise(cls, 
                         customs_value: Decimal, 
                         category: ExciseCategory, 
                         custom_rate: Decimal = None,
                         specific_rate_amount: Decimal = Decimal('0.00'),
                         volume_units: Decimal = Decimal('0.00')
                         ) -> Decimal:
        """
        Calculate the excise tax liability based on the goods category.
        
        Assumptions & Limitations:
        1. Base Ad Valorem: Excise is typically calculated on (Customs Value + Duty). 
           For V2 deterministic forecasting, this engine assumes the `customs_value` 
           provided here *already includes* applied duties if applicable to the scenario.
        2. Mixed Specific/Ad Valorem: If `specific_rate_amount` is provided, 
           the calculation incorporates both (e.g. $2 per liter + 10% value).
        3. Demo Boundaries: These baseline rates reflect analytical defaults, not 
           live regulatory tables which fluctuate politically.
        """
        if customs_value < 0 or specific_rate_amount < 0 or volume_units < 0:
            raise ValueError("Values and rates cannot be negative.")

        if category == ExciseCategory.EXEMPT:
            return Decimal("0.00")

        # Use custom rate if provided (e.g., during What-If scenarios), otherwise default
        rate = custom_rate if custom_rate is not None else cls.DEFAULT_RATES.get(category, Decimal("0.00"))

        # Ad Valorem component
        ad_valorem_tax = customs_value * rate

        # Specific component (e.g. $1.50 per unit/liter/pack)
        specific_tax = specific_rate_amount * volume_units

        total_excise = ad_valorem_tax + specific_tax

        # Standard financial rounding
        return total_excise.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
