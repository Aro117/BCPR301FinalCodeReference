from __future__ import print_function
import sys
from abc import ABCMeta, abstractmethod
import re
import datetime as date



class IFileValidator(metaclass=ABCMeta):
    @abstractmethod
    def check_data_set(self, data_set):
        pass

    @abstractmethod
    def check_line(self, employee_attributes):
        pass

    @abstractmethod
    def check_all(self, employee_attributes):
        pass

    @abstractmethod
    def check_id(self, emp_id):
        pass

    @abstractmethod
    def check_age(self, age):
        pass

    @abstractmethod
    def check_sales(self, sales):
        pass

    @abstractmethod
    def check_bmi(self, bmi):
        pass

    @abstractmethod
    def check_salary(self, salary):
        pass

    @abstractmethod
    def check_birthday(self, birthday):
        pass

    @abstractmethod
    def check_gender(self, gender):
        pass

    @abstractmethod
    def check_birthday_against_age(self, birthday, age):
        pass


class Validator(IFileValidator):

    # Tim
    def __init__(self):
        self.id_rule = "^[A-Z][0-9]{3}$"
        self.gender_rule = "^(M|F)$"
        self.age_rule = "^[0-9]{2}$"
        self.sales_rule = "^[0-9]{3}$"
        self.bmi_rule = "^(Normal|Overweight|Obesity|Underweight)$"
        self.salary_rule = "^[0-9]{2,3}$"
        self.birthday_rule = "^[1-31]-[1-12]-[0-9]{4}$"
        self.attributes = {"EMPID", "GENDER", "AGE", "SALES", "BMI", "SALARY", "BIRTHDAY"}
        self.number_of_attributes = len(self.attributes)

    # Tim
    def set_rules(self, rules):
        try:
            self.id_rule = rules['id']
            self.gender_rule = rules['gender']
            self.age_rule = rules['age']
            self.sales_rule = rules['sales']
            self.bmi_rule = rules['bmi']
            self.salary_rule = rules['salary']
        except KeyError as missing_key:
            print('The key {} was missing from the rules.txt file'.format(missing_key), file=sys.stderr)

    # Tim
    def check_data_set(self, data_set):
        # Should be of form [{EMPID: B12, GENDER: M, AGE: 22, etc}, {EMPID: 55Y, GENDER: F, etc}]
        if len(data_set) == 0:
            print('The data was empty', file=sys.stderr)
            return False
        else:
            for employee in data_set:
                if not self.check_line(employee):
                    print('One or more of the lines of data was invalid', file=sys.stderr)
                    return False
        # Failing to invalidate is a success
        return True

    # Tim
    def check_line(self, employee_attributes):
        # Should be of form {EMPID: B12, GENDER: M, AGE: 22, etc}
        for attribute in self.attributes:
            if attribute not in employee_attributes:
                print('Missing attribute: {}'.format(attribute), file=sys.stderr)
                return False
        try:
            if not self.check_all(employee_attributes):
                return False
        except TypeError:
            print('The data was not bundled correctly', file=sys.stderr)
            return False
        # Failing to invalidate is a success
        return True

    # Rosemary
    def check_all(self, employee_attributes):
        if not self.check_birthday(employee_attributes["BIRTHDAY"]):
            return False
        if not self.check_id(employee_attributes["EMPID"]):
            return False
        if not self.check_age(employee_attributes["AGE"]):
            return False
        if not self.check_gender(employee_attributes["GENDER"]):
            return False
        if not self.check_sales(employee_attributes["SALES"]):
            return False
        if not self.check_bmi(employee_attributes["BMI"]):
            return False
        if not self.check_salary(employee_attributes["SALARY"]):
            return False
        if not self.check_birthday_against_age(employee_attributes["BIRTHDAY"], employee_attributes["AGE"]):
            return False
        return True

    def check_hud(self, rule, value):

        try:
            if not re.match(rule, value):
                print('{} is invalid!'.format(value), file=sys.stderr)
                return False
            else:
                return True
        except TypeError:
            return False

    # Rosemary
    def check_id(self, emp_id):
        if not self.check_hud(self.id_rule, str(emp_id)):
            return False
        return True

    def check_age(self, age):
        # Should be between 1-99
        if not self.check_hud(self.age_rule, str(age)):
            return False
        return True


    def check_gender(self, gender):
        if not self.check_hud(self.gender_rule, str(gender)):
            return False
        return True

    # Rosemary
    def check_sales(self, sales):
        if not self.check_hud(self.sales_rule, str(sales)):
            return False
        return True

    # Hasitha
    def check_bmi(self, bmi):
        if not self.check_hud(self.bmi_rule, str(bmi)):
            return False
        return True

    # Hasitha
    def check_salary(self, salary):
        if not self.check_hud(self.salary_rule, str(salary)):
            return False
        return True

    # Tim
    def check_birthday(self, birthday):
        try:
            day_month_year = birthday.split("-")
            day = int(day_month_year[0])
            month = int(day_month_year[1])
            year = int(day_month_year[2])
            date.datetime(year, month, day)
            return True
        except ValueError:
            print('The date was invalid', file=sys.stderr)
            return False
        except AttributeError:
            print('The date was in an invalid format', file=sys.stderr)
            return False

    # Tim
    def check_birthday_against_age(self, birthday, age):

        if not self.check_birthday(birthday):
            return False
        else:
            day_month_year = birthday.split("-")
            day = int(day_month_year[0])
            month = int(day_month_year[1])
            year = int(day_month_year[2])
            # adding age because we just want to compare month and day
            birth = date.datetime(year, month, day)
            today = date.datetime.today()
            if birth.month < today.month:
                # Had a birthday already this year
                return int(age) == today.year - year
            elif birth.month == today.month and birth.day < today.day:
                # Had a birthday already this year (this month)
                return int(age) == today.year - year
            else:
                # Hasn't had a birthday yet this year.
                return int(age) == today.year - year - 1

    # Tim
    def check_in_attributes(self, query_attribute):

        try:
            return query_attribute.upper() in self.attributes
        except AttributeError:
            return False

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=0)
