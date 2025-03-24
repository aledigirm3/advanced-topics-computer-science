from dataclasses import dataclass

@dataclass
class dbExtractorExample:
    query: str
    answer: str

    def __str__(self):
        return f"""
        [QUERY]: 
        {self.query}
        [ANSWER]: 
        {self.answer}
        """
@dataclass
class TablesExtractorExample:
    query: str
    database1: str
    database2: str
    database3: str
    answer: str

    def __str__(self):
        return f"""
        [QUERY]: 
        {self.query}
        [DATABASE 1]:
        {self.database1}
        [DATABASE 2]:
        {self.database2}
        [DATABASE 3]:
        {self.database3}
        [ANSWER]: 
        {self.answer}
        """



findDB_example1 = dbExtractorExample(
    query="How many postal points with unique post office types are there in Ohio?",
    answer = "address, regional_sales, shipping, airline, retail_world,chicago_crime, public_review_platform, superstore, sales_in_weather, coinmarketcap"
)

findDB_example2 = dbExtractorExample(
    query="How many breweries are located in North America?",
    answer = "craftbeer, beer_factory, regional_sales, retail_world, chicago_crime, public_review_platform, superstore, sales_in_weather, coinmarketcap, food_inspection"
)

findDB_example3 = dbExtractorExample(
    query="When was the project with the highest quantity went live on the site? Indicate the grade level for which the project materials are intended.",
    answer = "software_company, cs_semester, computer_student, university, books, book_publishing_company, codebase_comments, authors, regional_sales"
)


findDB_example1DEV = dbExtractorExample(
    query="Who is the top spending customer and how much is the average price per single item purchased by this customer? What currency was being used?",
    answer="financial, debit_card_specializing, card_games"
)

findDB_example2DEV = dbExtractorExample(
    query="Which post has the highest score? Please give its id and title's name",
    answer="codebase_community, financial, student_club"
)

findDB_example3DEV = dbExtractorExample(
    query="What is the educational level name for the schools with Breakfast Provision 2 in county code 37? Indicate the name of the school.",
    answer="california_schools, student_club, financial"
)

findTables_example1DEV = TablesExtractorExample(
    query="",
    database1="",
    database2="",
    database3="",
    answer=""
)

findTables_example2DEV = TablesExtractorExample(
    query="",
    database1="",
    database2="",
    database3="",
    answer=""
)

findTables_example3DEV = TablesExtractorExample(
    query="",
    database1="",
    database2="",
    database3="",
    answer=""
)