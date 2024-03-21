# machine_learning_project/scripts/data_crawler.py

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd



def crawl_cuetracker():
    url = 'https://cuetracker.net'
    response = requests.get(url)
    
    if response.status_code == 200:
        # Save the raw HTML content to a file
        raw_html = response.text
        save_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'cuetracker_raw.html')
        with open(save_path, 'wt', encoding='utf-8') as f:  # Specify encoding as 'utf-8'
            f.write(raw_html)
            
        print("Raw HTML content saved to: {}".format(save_path))


def table():

    # URL of the webpage with the table
    #url = 'https://cuetracker.net/statistics/matches-and-frames/won/all-time'
    url ='https://www.snooker.org/res/index.asp?template=31'
    #url = 'https://en.wikipedia.org/wiki/Judd_Trump'

    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table element
        table = soup.find('table', class_="wikitable")
        
        # Extract data from the table
        data = []
        for row in table.find_all('tr'):
            row_data = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            data.append(row_data)
        
        # Create a pandas DataFrame from the extracted data
        df = pd.DataFrame(data[1:], columns=data[0])
        
        # Print the DataFrame
        print(df)
        
        # Optionally, you can save the DataFrame to a CSV file
        df.to_csv('cuetrackerjudd_trump_data.csv', index=False)
    else:
        print(f"Failed to fetch data from {url}")

def player_advancement():

    url = "https://en.wikipedia.org/wiki/Judd_Trump"

    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find the specific table containing player advancements in tournaments
        table = soup.find("table", class_="wikitable")

        # Read the table into a pandas DataFrame
        dfs = pd.read_html(str(table), flavor='bs4')
        
        # Process the DataFrame
        if len(dfs) > 0:
            df = dfs[0]  # Assuming the desired table is the first one found
            # Deal with colspan cells
            for col in df.columns:
                # Fill cells with colspan with the values from the cell above
                df[col] = df[col].fillna(method='ffill')
            # Remove rows with all NaN values
            df.dropna(how='all', inplace=True)
            # Reset the index
            df.reset_index(drop=True, inplace=True)
            
            # Print the DataFrame
            print(df)
            df.to_csv('cuetrackerjudd_trump_data.csv', index=False)

        else:
            print("No tables found on the webpage.")
    else:
        print("Failed to retrieve webpage.")

def player_recent_matches():
    url = "https://www.snooker.org/res/index.asp?player=12"
    #https://www.snooker.org/res/index.asp?player=12
    #https://www.snooker.org/res/index.asp?season=-1&player=12
    

    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all <tr> elements with class name starting with 'gradeA'
        tr_elements = soup.find_all("tr", class_=lambda x: x and x.startswith('gradeA even'))
        #print(tr_elements)

        thead_elements = soup.find_all('thead')
        #print(thead_element)
        for thead_element in thead_elements:
            # Find all <tr> elements under the current <thead> element
            in_tr_elements = thead_element.find_all('tr')
            for in_tr_element in in_tr_elements:
                    # Find all <a> elements under the current <tr> element with an href attribute starting with '/res'
                    a_elements = in_tr_element.find_all('a', href=lambda href: href and href.startswith('/res'))
                
                # Extract the text from each <a> element
                    for a_element in a_elements:
                        headers = a_element.get_text(strip=True)
                        print(headers)
            


        # Find the <a> element within the <thead> element
        # Find all <a> elements
        #a_elements = soup.find_all('a')
        a_elements = soup.find_all('a', href=lambda i: i and i.startswith('/res'))


        # Extract the text from each <a> element
        for a_element in a_elements: 
            text = a_element.get_text(strip=True)
            #print(text)
        
        
        # Extract titles from the <td> elements within the selected <tr> elements
        for tr in tr_elements:
            # Find all <td> elements within the <tr> element
            td_elements = tr.find_all("td")

            
            titles = [td.text.strip() for td in td_elements if td.get('class') and 'round' in td.get('class')]
            if titles:
                print(titles[0])
            
            '''first_score = [td.text.strip() for td in td_elements if td.get('class') and 'score  first-score' in td.get('class')]
            if first_score:
                print(first_score)

            last_score = [td.text.strip() for td in td_elements if td.get('class') and 'last-score' in td.get('class')]
            if first_score:
                print(last_score)
            '''

            first_score = td_elements[3].text.strip()
            last_score = td_elements[5].text.strip()

            print(first_score,last_score)

            player_names = [td.text.strip() for td in td_elements if td.get('class') and 'player' in td.get('class')]
            if player_names:
                pass
                print(player_names[0], ' ', player_names[1])

               
            
         
    else:
        print("Failed to retrieve webpage.")

def get_table_elements():

    url = "https://www.snooker.org/res/index.asp?player=12"
    #https://www.snooker.org/res/index.asp?player=12
    #https://www.snooker.org/res/index.asp?season=-1&player=12
    

    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table element
        table = soup.find('table', class_='display matches')

        '''# Iterate through the children of the table
        for child in table.children:

            # Check if the child is a thead or tbody element
            if child.name == 'thead' or child.name == 'tbody':

                # Find all the text within the child element
                text = child.get_text(strip=True)
                print(text)
        '''

        if table:
            # Find all thead and tbody elements within the table
            thead_elements = table.find_all('thead')
            tbody_elements = table.find_all('tbody')
            print(tbody_elements[12])
            
            # Iterate over the pairs of thead and tbody elements
            for thead, tbody in zip(thead_elements, tbody_elements):
                # Extract text from the thead element
                thead_text = thead.get_text(strip=True)
                print(thead_text)
                tbodytext = tbody.get_text(strip=True)

                #next_tbody = thead.find_next_sibling('tbody')
        
                # Check if next_tbody is found
                if tbody:
                # Find all tr elements with class starting with "gradeA" within the next tbody sibling
                    tr_elements = tbody.find_all("tr", class_=lambda c: c and c.startswith('gradeA'))
                    #print(len(tr_elements))
            
                    # Iterate over the tr elements
                    for tr in tr_elements:
                        # Find all <td> elements within the <tr> element
                        td_elements = tr.find_all("td")
                
                        # Extract text from all <td> elements within the tr
                        titles = [td.text.strip() for td in td_elements if td.get('class') and 'round' in td.get('class')]
                        #print(titles[0])
                        
           


        else:
            print("Table with class 'display matches' not found.")

def get_it():
        
    url = "https://www.snooker.org/res/index.asp?player=12"
        #https://www.snooker.org/res/index.asp?player=12
        #https://www.snooker.org/res/index.asp?season=-1&player=12
    

        # Send a GET request to the webpage
    response = requests.get(url)

        # Check if the request was successful
    if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the table element
            table = soup.find('table', class_='display matches')
        
            if table:
                # Find all thead elements within the table
                thead_elements = table.find_all('thead')
        
                # Iterate over the thead elements
                for i in range(len(thead_elements) - 1):
                    # Extract text from the thead element
                    thead_text = thead_elements[i].get_text(strip=True)
                    print(thead_text)
            
                    # Find all tr elements between this thead and the next one
                    tr_elements = thead_elements[i].find_all_next("tr", class_=lambda c: c and c.startswith('gradeA'), until=thead_elements[i + 1])
                    print(len(tr_elements))
                    print(thead_elements[i+1].get_text(strip=True))
            
                    # Iterate over the tr elements
                    for tr in tr_elements:
                        # Find all <td> elements within the <tr> element
                        td_elements = tr.find_all("td")
                
                        # Extract text from all <td> elements within the tr
                        titles = [td.text.strip() for td in td_elements if td.get('class') and 'round' in td.get('class')]
                        print(titles[0])
            else:
                print("Table with class 'display matches' not found.")


            
if __name__ == "__main__":
    #crawl_cuetracker()
    #table()
    #player_advancement()
    #player_recent_matches()
    get_table_elements()
    #get_it()
