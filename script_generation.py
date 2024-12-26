
# class ScriptGeneration:
#     def __init__(self, insights):
#         self.insights = insights

#     def generate_script(self):
#         script = (
#             f"20% of users use iPhone and 30% of users use Samsung. "
#             f"According to our data, {self.insights['iphone_percentage']}% of users use iPhone, "
#             f"and {self.insights['samsung_percentage']}% of users use Samsung."
#         )
#         return script

# # Example usage
# if __name__ == "__main__":
#     from data_processing import DataProcessing
#     from data_ingestion import DataIngestion

#     ingestion = DataIngestion("path_to_your_csv_file.csv")
#     data = ingestion.read_csv()

#     if data is not None:
#         processing = DataProcessing(data)
#         insights = processing.process_data()

#         script_gen = ScriptGeneration(insights)
#         script = script_gen.generate_script()
#         print(script)