from src.crud.week_plan import create_weekplan_entry

async def create_weekplan(plan, city):
    """
    plan format : {'Monday': [promotion_id], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
    """
    for day in plan.keys():
        for promo in plan[day]:
            create_weekplan_entry(day, promo, city)
    return 'Created'