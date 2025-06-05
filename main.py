import data
import helpers

class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

    def test_set_route(self):
        print("test_set_route function is ready")
        pass

    def test_select_plan(self):
        print("test_select_plan function is ready")
        pass

    def test_fill_phone_number(self):
        print("test_fill_phone_number function is ready")
        pass

    def test_fill_card(self):
        print("test_fill_card function is ready")
        pass

    def test_comment_for_driver(self):
        print("test_comment_for_driver function is ready")
        pass

    def test_order_blanket_and_handkerchiefs(self):
        print("test_order_blanket_and_handkerchiefs function is ready")
        pass

    def test_order_2_ice_creams(self):
        print("test_order_2_ice_creams function is ready")
        for _ in range(2):
            # Add in S8
            pass

    def test_car_search_model_appears(self):
        print("test_car_search_model_appears function is ready")
        pass
