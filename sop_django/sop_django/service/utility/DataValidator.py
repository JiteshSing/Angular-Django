import re
class DataValidator:

    @classmethod
    def isNotNull(Virendra,val):
        if(val == None or val == ""):
            return False
        else:
            return True

    @classmethod
    def isNull(virendra,val):
        if(val == None or val == ""):
            return True
        else:
            return False

    @classmethod
    def isInt(self,val):
        if(val == 0):
            return False
        else:
            return True

    @classmethod
    def ismobilecheck(self,val):
        if re.match("^[6-9]\d{9}$",val):
            return False
        else:
            return True

    @classmethod
    def validate_two_decimal(self, val):
        str_value = str(val)
        decimal_part = str_value.split('.')[1]
        # Check if the decimal part has more than 2 digits
        if len(decimal_part) < 3:
            return False
        else:
            return True

    @classmethod
    def max_len_10(self, val):
        if len(str(val)) <= 10:
            return False
        else:
            return True

    @classmethod
    def isflt(self, val):
        try:
            float(val)
            return False
        except ValueError:
            return True

    @classmethod
    def max_len_100(self, val):
        if len(str(val)) <= 100:
            return False
        else:
            return True

    @classmethod
    def is_0(self, val):
        if int(val) <= 0:
            return True
        else:
            return False

    @classmethod
    def max_len_5(self, val):
        if len(str(val)) <= 5:
            return False
        else:
            return True

    @classmethod
    def isalphanumeric(self, val):
        if str(val).isalnum():
            return False
        else:
            return True

    @classmethod
    def len_btw_3_to_30(self, val):
        if 3 <= len(str(val)) <= 50:
            return False
        else:
            return True

    @classmethod
    def len_btw_10_to_200(self, val):
        if 10 <= len(str(val)) <= 200:
            return False
        else:
            return True