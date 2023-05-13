from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, desc, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Query
from io import StringIO
import csv

NUM_FORMAT_MSG = "(in the format '987654321')"
Base = declarative_base()


class Companies(Base):
    __tablename__ = "companies"

    ticker = Column(String(10), primary_key=True)
    name = Column(String(30))
    sector = Column(String(30))


class Financial(Base):
    __tablename__ = "financial"

    ticker = Column(String(10), primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)


class DBHelper:
    def __init__(self, filename):
        self.filename = filename
        self.engine = create_engine(f"sqlite:///{filename}", echo=False)
        self.conn = self.engine.connect()
        self.Base = Base
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def import_csv(self, class_name, file_name):
        list_to_add = []
        not_added = []  # implement a notice later for entries not added due to pk conflict
        with open(file_name, "r") as file:
            csv_reader = csv.DictReader(file)
            for dict_entry in csv_reader:
                # skip if it exists and add to not_added
                if self.session.query(class_name).filter(class_name.ticker == dict_entry["ticker"]).first():
                    not_added.append(dict_entry)
                    continue
                current_entry = class_name()  # can be changed to **dict to unpack in future
                for column, value in dict_entry.items():
                    if value:
                        setattr(current_entry, column, value)
                    else:
                        setattr(current_entry, column, None)
                list_to_add.append(current_entry)
        self.session.add_all(list_to_add)
        self.safe_commit()

    def safe_commit(self):
        try:
            self.session.commit()
        except Exception as e:
            print(e, "\n\nPlease fix the issues above and try again")
            self.session.rollback()
            self.session = self.Session()


class Menu:
    def __init__(self, title: str, options: list, parent_menu=None, child_menu=None):
        self.title = title
        self.options = options  # options define menu options and functions as a tuple
        self.parent_menu = parent_menu
        self.child_menu = child_menu
        self.INPUT_MESSAGE = "Enter an option:\n"
        self.MENU_ERROR = "Invalid option!\n"
        self.EXIT_MESSAGE = "Have a nice day!"
        self.OPTIONS_STRING = self.create_options_string()

    def ask_user_option(self):
        user_input = -1
        while user_input < 0 or user_input >= len(self.options):
            try:
                print(self.OPTIONS_STRING)
                user_input = int(input(self.INPUT_MESSAGE))
                if user_input >= len(self.options) or user_input < 0:
                    raise OptionNotInRange
                else:
                    self.options[user_input][1]()
            except ValueError:
                print("Invalid option!\n")
                if self.parent_menu:
                    self.parent_menu.ask_user_option()
                    break
            except OptionNotInRange as e:
                print(e)
                if self.parent_menu:
                    self.parent_menu.ask_user_option()
                    break

    def create_options_string(self):
        output = StringIO()
        if self.title:
            output.write(F"{self.title}\n")
        option_counter = 0
        for option in self.options:
            output.write(f"{option_counter} {option[0]}\n")
            option_counter += 1
        return output.getvalue()

    def not_implemented(self):
        print("Not implemented!\n")
        self.back()

    def exit(self):
        print(self.EXIT_MESSAGE)

    def back(self):
        self.parent_menu.ask_user_option()


class MainMenu(Menu):
    def __init__(self, db_helper: DBHelper):
        options = [("Exit", self.exit),
                   ("CRUD operations", self.crud_menu),
                   ("Show top ten companies by criteria", self.top_ten_menu)]
        super().__init__("MAIN MENU", options)
        self.db_helper = db_helper

    def crud_menu(self):
        self.child_menu = CRUDMenu(self.db_helper, parent_menu=self)
        self.child_menu.ask_user_option()

    def top_ten_menu(self):
        self.child_menu = TopTenMenu(self.db_helper, parent_menu=self)
        self.child_menu.ask_user_option()


class CRUDMenu(Menu):
    def __init__(self, db_helper: DBHelper, parent_menu=None):
        options = [("Back", self.back),
                   ("Create a company", self.create_company),
                   ("Read a company", self.read_company),
                   ("Update a company", self.update_company),
                   ("Delete a company", self.delete_company),
                   ("List all companies", self.list_all)]
        super().__init__("CRUD MENU", options, parent_menu=parent_menu)
        self.db_helper = db_helper

    def create_company(self):  # implement data integrity checks later and db update check
        ticker = input("Enter ticker (in the format 'MOON'):\n")
        name = input("Enter company (in the format 'Moon Corp'):\n")
        sector = input("Enter industries (in the format 'Technology'):\n")
        financial_dict = create_financial_dict(ticker)
        self.db_helper.session.add(Companies(ticker=ticker, name=name, sector=sector))
        self.db_helper.session.add(Financial(**financial_dict))
        self.db_helper.safe_commit()
        print("Company created successfully!")
        self.back()

    def read_company(self):
        self.company_operation(self.read_company_function)

    def read_company_function(self, company):
        def print_company_stats():
            financial = self.db_helper.session.query(Financial).filter(Financial.ticker == company.ticker).one()
            print(company.ticker, company.name)
            p_e = None if None in [financial.market_price, financial.net_profit] \
                else f"{financial.market_price / financial.net_profit :.2f}"
            p_s = None if None in [financial.market_price, financial.sales] \
                else f"{financial.market_price / financial.sales :.2f}"
            p_b = None if None in [financial.market_price, financial.assets] \
                else f"{financial.market_price / financial.assets :.2f}"
            nd_e = None if None in [financial.net_debt, financial.ebitda] \
                else f"{financial.net_debt / financial.ebitda :.2f}"
            roe = None if None in [financial.net_profit, financial.equity] \
                else f"{financial.net_profit / financial.equity :.2f}"
            roa = None if None in [financial.net_profit, financial.assets] \
                else f"{financial.net_profit / financial.assets :.2f}"
            l_a = None if None in [financial.liabilities, financial.assets] \
                else f"{financial.liabilities / financial.assets :.2f}"
            print(f"P/E = {p_e}")
            print(f"P/S = {p_s}")
            print(f"P/B = {p_b}")
            print(f"ND/EBITDA = {nd_e}")
            print(f"ROE = {roe}")
            print(f"ROA = {roa}")
            print(f"L/A = {l_a}\n\n")
            self.back()
        return print_company_stats

    def update_company(self):
        self.company_operation(self.update_company_function)

    def update_company_function(self, company):
        def update_financials():
            financial_filter = self.db_helper.session.query(Financial).filter(Financial.ticker == company.ticker)
            new_financial = create_financial_dict(company.ticker)
            financial_filter.update(new_financial)
            self.db_helper.safe_commit()
            print("Company updated successfully!\n")
            self.back()
        return update_financials

    def delete_company(self):
        self.company_operation(self.delete_company_function)

    def delete_company_function(self, company):
        def delete_company():
            self.db_helper.session.query(Financial).filter(Financial.ticker == company.ticker).delete()
            self.db_helper.session.query(Companies).filter(Companies.ticker == company.ticker).delete()
            self.db_helper.safe_commit()
            print("Company deleted successfully!\n")
            self.back()
        return delete_company

    def list_all(self):
        print("COMPANY LIST")
        company_list = self.db_helper.session.query(Companies).order_by(Companies.ticker).all()
        for company in company_list:
            print(company.ticker, company.name, company.sector)
        print("")
        self.back()

    def company_operation(self, rud_function):
        name = input("Enter company name:\n")
        company_list = self.db_helper.session.query(Companies).filter(Companies.name.ilike(f"%{name}%")).all()
        if company_list:
            company_options = map(lambda comp: (comp.name, rud_function(comp)), company_list)
            company_menu = Menu("", list(company_options))
            company_menu.INPUT_MESSAGE = "Enter company number:\n"
            company_menu.ask_user_option()
        else:
            print("Company not found!\n")


class TopTenMenu(Menu):
    def __init__(self, db_helper: DBHelper, parent_menu=None):
        options = [("Back", self.back),
                   ("List by ND/EBITDA", self.list_nd_e),
                   ("List by ROE", self.list_roe),
                   ("List by ROA", self.list_roa)]
        super().__init__("TOP TEN MENU", options, parent_menu=parent_menu)
        self.db_helper = db_helper

    def get_top_ten(self, metric: str):
        if metric == "nd_e":
            sort_by = Financial.net_debt / Financial.ebitda
            header = "ND/EBITDA"
        elif metric == "roe":
            sort_by = Financial.net_profit / Financial.equity
            header = "ROE"
        else:
            sort_by = func.round(Financial.net_profit / Financial.assets, 2)
            header = "ROA"

        top_ten_list = self.db_helper.session.query(Financial.ticker, sort_by.label("value"))\
                           .order_by(desc(sort_by))[:10]
        print(f"TICKER {header}")
        for entry in top_ten_list:
            print(entry.ticker, f"{entry.value:.2f}".rstrip("0."))
        self.back()

    def list_nd_e(self):
        self.get_top_ten("nd_e")

    def list_roe(self):
        self.get_top_ten("roe")

    def list_roa(self):
        self.get_top_ten("roa")


class OptionNotInRange(Exception):
    def __init__(self):
        super().__init__("Invalid option!\n")


def create_financial_dict(ticker: str):
    financial_dict = dict(ticker=ticker)
    financial_dict["ebitda"] = input(f"Enter ebitda {NUM_FORMAT_MSG}:\n")
    financial_dict["sales"] = input(f"Enter sales {NUM_FORMAT_MSG}:\n")
    financial_dict["net_profit"] = input(f"Enter net profit {NUM_FORMAT_MSG}:\n")
    financial_dict["market_price"] = input(f"Enter market price {NUM_FORMAT_MSG}:\n")
    financial_dict["net_debt"] = input(f"Enter net debt {NUM_FORMAT_MSG}:\n")
    financial_dict["assets"] = input(f"Enter assets {NUM_FORMAT_MSG}:\n")
    financial_dict["equity"] = input(f"Enter equity {NUM_FORMAT_MSG}:\n")
    financial_dict["cash_equivalents"] = input(f"Enter cash equivalents {NUM_FORMAT_MSG}:\n")
    financial_dict["liabilities"] = input(f"Enter liabilities {NUM_FORMAT_MSG}:\n")
    return financial_dict


if __name__ == "__main__":
    my_db_helper = DBHelper("investor.db")
    # my_db_helper.import_csv(Companies, "test\\companies.csv")
    # my_db_helper.import_csv(Financial, "test\\financial.csv")
    # print("Database created successfully!")
    print("Welcome to the Investor Program!\n")
    my_menu = MainMenu(my_db_helper)
    my_menu.ask_user_option()
