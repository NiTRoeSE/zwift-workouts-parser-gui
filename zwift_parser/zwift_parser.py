from zwift_parser.zwift_workout import ZWorkout, ZWorkoutParseMode

class Parser:
    """
    A class is used to parse any **bike** zwift workout, presented on the 
    www.whatsonzwift.com

    Modified version of zwift-workouts-parser to get the normally printed results back to use Parser class directly in swp.py
    Added self.result array and append all prints to this array, moved executing function from init to separated
    get_results function because return in init ist not possible.

    Why this? 
    In builded flet a external python script call with subprocess combined with python xyz.py is not possible because no python executable is usable.

    -- NiTRoSoft | SWP GUI
    """

    def __init__(self, export_dir, urls, skip: bool = False, replace: bool = False) -> None:
        """
        Parameters 
        ----------
        export_dir : str 
                The folder that is used to save all the parsed workouts. 
        urls : List[str]
                A list of urls that need to be parsed, can be either a 
                direct link to a single workout, plan or a page which 
                contains multiple plans/workouts. 
        skip : Bool 
                Should the workouts that can be downloaded be skipped by
                the parser? 
        replace : Bool 
                Should the workouts that can be downloaded be replaced with
                the files uploaded to the site? 
        """

        self.export_dir = export_dir
        self.skip = skip 
        self.replace = replace
        self.result = [] 
        
    
    def __try_parse(self, url):
        parsed = self.__try_parse_plans(url); 
        if not parsed: 
            parsed = self.__try_parse_workout(url);  
        return parsed 

    def __try_parse_plans(self, url):
        plans_data = Parser.__get_web_content(url, 'div', 'card')
        if not plans_data: return False;   
        any_parsed = False  
        for i, plan_data in enumerate(plans_data):
            card_sports = plan_data.find('div', class_='card-sports')
            if not card_sports: continue

            card_classes = card_sports.i['class']
            valid = ZWorkout.is_valid_sport_type(card_classes) 
            url = plan_data.find('a', class_='button')['href']

            if not valid: 
                print(f"Couldn't parse {url} because some of the {card_classes} sports are not suppored yet")
                self.result.append(f"Couldn't parse {url} because some of the {card_classes} sports are not suppored yet") 
                continue

            print(f"Parsing plan ({i+1}/{len(plans_data)})")
            self.result.append(f"Parsing plan ({i+1}/{len(plans_data)})") 
            self.__try_parse_workout(url)
            any_parsed = True 
        return any_parsed 

    def __try_parse_workout(self, url):
        workouts_data = Parser.__get_web_content(url, 'article', 'workout')
        if not workouts_data: 
            print(f"Couldn't get workout data by {url} for unknown reason.")
            self.result.append(f"Couldn't get workout data by {url} for unknown reason.") 
            return False 

        for i, workout_data in enumerate(workouts_data): 
            print(f"- Parsing workout ({i+1}/{len(workouts_data)})")
            self.result.append(f"- Parsing workout ({i+1}/{len(workouts_data)})") 

            mode = ZWorkoutParseMode.DEFAULT
            if self.skip: mode = ZWorkoutParseMode.SKIP
            elif self.replace: mode = ZWorkoutParseMode.REPLACE
            """ modified zwift_workout.py to return the processing results and collect it in self.result """
            result = ZWorkout(workout_data, mode).save(self.export_dir)
            self.result.append(result) 
            #print(f"**{result}**")
        return True 

    def __get_web_content(url, tag, tag_class):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Vivaldi/4.3',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

        import ssl, certifi, urllib.request
        req = urllib.request.Request(url, headers=headers)
        context = ssl.create_default_context(cafile=certifi.where())
        response = urllib.request.urlopen(req, context=context)
        content =  response.read().decode('utf-8')

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, features='html.parser')
        return soup.find_all(tag, class_ = tag_class)

    def get_result(self,urls):
        for i, url in enumerate(urls): 
            print(f'Parsing url {url} ({i+1}/{len(urls)})')
            parsed = self.__try_parse(url) 
            if not parsed: 
                print(f"Couldn't find a parser for {url} hence skipping it.")
                self.result.append(f"Couldn't find a parser for {url} hence skipping it.") 

                continue
        return self.result