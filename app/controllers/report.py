from ..repositories.managers import IngredientManager, OrderDetailManager, OrderManager
from .base import BaseController
import datetime 

class ReportController(BaseController):

    @classmethod
    def get_report(cls):
        orders = OrderManager.get_all()
        order_details = OrderDetailManager.get_all()
        ingredient_name = IngredientManager.get_all()
        all_ingredients_list = [orderDetail["ingredient"]['_id']
                                     for orderDetail in order_details]
        most_request_ingredient = max(set(all_ingredients_list), key=all_ingredients_list.count, default=0)
        most_request_ingredient_name = [ingredient["name"] for ingredient in ingredient_name if ingredient["_id"] == most_request_ingredient][0] if most_request_ingredient else None
        all_months_dict = {}
        for order in orders:
            get_selected_month = datetime.datetime.strptime(order["date"], '%Y-%m-%dT%H:%M:%S').month
            all_months_dict[get_selected_month] = float("{:.2f}".format(round(all_months_dict.get(get_selected_month, 0) + order['total_price'],2)))

        max_month_revenue = max(all_months_dict, key=all_months_dict.get, default=0)
        max_revenue = max(all_months_dict.values(), default=0)

        all_clients_dict = {}
        for order in orders:
            
            all_clients_dict[f"id:{order['client_dni']} name:{order['client_name']}"] = float("{:.2f}".format(round(all_clients_dict.get(f"id:{order['client_dni']} name:{order['client_name']}", 0) + order['total_price'], 2)))

        top3_clients = sorted(all_clients_dict, key=all_clients_dict.get, reverse=True)[:3]
        top3_clients_values = sorted(all_clients_dict.values(), reverse=True)[:3]

        reports = {'most_requested_ingredient': f'id:{most_request_ingredient} name:{most_request_ingredient_name}', 'most_revenue_month': max_month_revenue, 'max_revenue': "{:.2f}".format(max_revenue), 'top_3_customers': top3_clients, 'top_3_customers_values': list(map(lambda x: "{:.2f}".format(x), top3_clients_values)) }

        return reports, None
