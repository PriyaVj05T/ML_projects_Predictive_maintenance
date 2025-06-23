import sys

class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = error_message

        # unpacking of traceback info
        _, _, exc_tb = error_details.exc_info()

        # attribute names
        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        # string formatting using correct attributes
        return f"Error occurred in Python script [{self.filename}], line number [{self.lineno}], error message [{self.error_message}]"


if __name__== "__main__":

    try:
        a=1/0

    except Exception as e :
       raise CustomException(e,sys)


