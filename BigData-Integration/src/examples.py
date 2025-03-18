from dataclasses import dataclass

@dataclass
class TaskExample:
    query: str
    answer: str

    def __str__(self):
        return f"""
        [QUERY]: 
        {self.query}
        [ANSWER]: 
        {self.answer}
        """


findDB_example1 = TaskExample(
    query="How many postal points with unique post office types are there in Ohio?",
    answer = "address, regional_sales, shipping, airline, retail_world,chicago_crime, public_review_platform, superstore, sales_in_weather, coinmarketcap"
)

findDB_example2 = TaskExample(
    query="How many breweries are located in North America?",
    answer = "craftbeer, beer_factory, regional_sales, retail_world, chicago_crime, public_review_platform, superstore, sales_in_weather, coinmarketcap, food_inspection"
)

findDB_example3 = TaskExample(
    query="When was the project with the highest quantity went live on the site? Indicate the grade level for which the project materials are intended.",
    answer = "software_company, cs_semester, computer_student, university, books, book_publishing_company, codebase_comments, authors, regional_sales"
)