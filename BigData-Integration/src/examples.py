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
        [DATABASES]:
        {self.database1}
        {self.database2}
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
    query="Describe the names of neutral alignment superheroes.",
    database1="superhero: alignment, attribute, colour, gender, publisher, race, superhero, hero attribute, superpower, hero power",
    database2="student_club: Event, Major, Zip Code, Attendance, Budget, Expense, Income, Member",
    database3="codebase_community: badges, comments, post History, post Links, posts, tags, users, votes",
    answer="superhero: hero attribute, attribute"
)

findTables_example2DEV = TablesExtractorExample(
    query="How many bond id have element iodine?",
    database1="formula_1: circuits, constructors, drivers, seasons, races, constructor results, constructor standings, driver standings, lap times, pit stops, qualifying, status, results",
    database2="thrombosis_prediction: Examination, Patient, Laboratory",
    database3="toxicology: atom, bond, connected, molecule",
    answer="toxicology: atom, molecule"
)

findTables_example3DEV = TablesExtractorExample(
    query="Please list the lowest three eligible free rates for students aged 5-17 in continuation schools.",
    database1="student_club: Event, Major, Zip Code, Attendance, Budget, Expense, Income, Member",
    database2="california_schools: free and reduced-price meals, sat scores, schools",
    database3="financial: account, card, client, disposition, district, loan, order, transaction",
    answer="california_schools: free and reduced-price meals"
)

att_findTables_example1DEV = TablesExtractorExample(
    query="List the heroes' names whose eyes and hair colours are both black.",
    database1="superhero: alignment(id, alignment), attribute(id, attribute_name), colour(id, colour), gender(id, gender), publisher(id, publisher_name), race(id, race), superhero(id, superhero_name, full_name, gender_id, eye_colour_id, hair_colour_id, skin_colour_id, race_id, publisher_id, alignment_id, height_cm, weight_kg), hero attribute(hero_id, attribute_id, attribute_value), superpower(id, power_name), hero power(hero_id, power_id)",
    database2="codebase_community: badges(Id, UserId, Name, Date), comments(Id, PostId, Score, Text, CreationDate, UserId, UserDisplayName), post History(Id, PostHistoryTypeId, PostId, RevisionGUID, CreationDate, UserId, Text, Comment, UserDisplayName), post Links(Id, CreationDate, PostId, RelatedPostId, LinkTypeId), tags(Id, TagName, Count, ExcerptPostId, WikiPostId), users(Id, Reputation, CreationDate, DisplayName, LastAccessDate, WebsiteUrl, Location, AboutMe, Views, UpVotes, DownVotes, AccountId, Age, ProfileImageUrl), votes(Id, PostId, VoteTypeId, CreationDate, UserId, BountyAmount)",
    database3="student_club: Event(event_id, event_name, event_date, type, notes, location, status), Major(major_id, major_name, department, college), Zip Code(zip_code, type, city, county, state, short_state), Attendance(link_to_event, link_to_member), Budget(budget_id, category, spent, remaining, amount, event_status, link_to_event), Expense(expense_id, expense_description, expense_date, cost, approved, link_to_member, link_to_budget), Income(income_id, date_received, amount, source, notes, link_to_member), Member(member_id, first_name, last_name, email, position, t_shirt_size, phone, zip, link_to_major)",
    answer="superhero: superhero(superhero_name, eye_colour_id, hair_colour_id), colour(id, colour)"
)

att_findTables_example2DEV = TablesExtractorExample(
    query="How many users last accessed the website after 2014/9/1?",
    database1="debit_card_specializing: customers(CustomerID, Segment, Currency), gas stations(GasStationID, ChainID, Country, Segment), products(ProductID, Description), transactions(TransactionID, Date, Time, CustomerID, CardID, GasStationID, ProductID, Amount, Price), year and month(CustomerID, Date, Consumption)",
    database2="codebase_community: badges(Id, UserId, Name, Date), comments(Id, PostId, Score, Text, CreationDate, UserId, UserDisplayName), post History(Id, PostHistoryTypeId, PostId, RevisionGUID, CreationDate, UserId, Text, Comment, UserDisplayName), post Links(Id, CreationDate, PostId, RelatedPostId, LinkTypeId), tags(Id, TagName, Count, ExcerptPostId, WikiPostId), users(Id, Reputation, CreationDate, DisplayName, LastAccessDate, WebsiteUrl, Location, AboutMe, Views, UpVotes, DownVotes, AccountId, Age, ProfileImageUrl), votes(Id, PostId, VoteTypeId, CreationDate, UserId, BountyAmount)",
    database3="student_club: Event(event_id, event_name, event_date, type, notes, location, status), Major(major_id, major_name, department, college), Zip Code(zip_code, type, city, county, state, short_state), Attendance(link_to_event, link_to_member), Budget(budget_id, category, spent, remaining, amount, event_status, link_to_event), Expense(expense_id, expense_description, expense_date, cost, approved, link_to_member, link_to_budget), Income(income_id, date_received, amount, source, notes, link_to_member), Member(member_id, first_name, last_name, email, position, t_shirt_size, phone, zip, link_to_major)",
    answer="codebase_community: users(Id, LastAccessDate)"
)