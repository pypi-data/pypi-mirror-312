import json
from io import StringIO
from typing  import Iterable
from loguru import logger

def convertstr(item):
    if isinstance(item, dict):
        return json.dumps(item)
    else:
        return str(item)

TEST_DATA = [
{"id":"1","name":"John","age":30,"city":"New York"},
{"id":"2","name":"Jane","age":25,"city":"Chicago"},
{"id":"3","name":"Bob","age":35,"city":"Los Angeles"},
{"id":"4","name":"Alice","age":28,"city":"San Francisco"},
{"id":"5","name":"Mike","age":32,"city":"Boston"},
{"id":"6","name":"Emily","age":27,"city":"Seattle"},
{"id":"7","name":"David","age":31,"city":"Houston"},
{"id":"8","name":"Sarah","age":29,"city":"Dallas"},
{"id":"9","name":"Chris","age":33,"city":"Miami"},
{"id":"10","name":"Linda","age":26,"city":"Atlanta"},
{"id":"11","name":"Tom","age":34,"city":"Philadelphia"},
{"id":"12","name":"Karen","age":30,"city":"Phoenix"},
{"id":"13","name":"Mark","age":31,"city":"San Diego"},
{"id":"14","name":"Jessica","age":32,"city":"Denver"},
{"id":"15","name":"Andrew","age":29,"city":"Detroit"},
{"id":"16","name":"Megan","age":28,"city":"Austin"},
{"id":"17","name":"Daniel","age":27,"city":"San Jose"},
{"id":"18","name":"Laura","age":26,"city":"Minneapolis"},
{"id":"19","name":"Steven","age":33,"city":"Columbus"},
{"id":"20","name":"Amy","age":30,"city":"Charlotte"},
{"id":"21","name":"Brian","age":31,"city":"Indianapolis"},
{"id":"22","name":"Rachel","age":32,"city":"Nashville"},
{"id":"23","name":"Jason","age":28,"city":"Louisville"},
{"id":"24","name":"Kim","age":27,"city":"Portland"},
{"id":"25","name":"Ryan","age":26,"city":"San Francisco"},
{"id":"26","name":"Emily","age":27,"city":"Seattle"},
{"id":"27","name":"David","age":31,"city":"Houston"},
{"id":"28","name":"Sarah","age":29,"city":"Dallas"},
{"id":"29","name":"Chris","age":30,"city":"Miami"},
{"id":"30","name":"Jennifer","age":32,"city":"Boston"},
{"id":"31","name":"Kevin","age":33,"city":"Philadelphia"},
{"id":"32","name":"Melissa","age":28,"city":"Atlanta"},
{"id":"33","name":"Eric","age":27,"city":"San Antonio"},
{"id":"34","name":"Jessica","age":26,"city":"Detroit"},
{"id":"35","name":"Andrew","age":31,"city":"San Diego"},
{"id":"36","name":"Amanda","age":30,"city":"Denver"},
{"id":"37","name":"Nicholas","age":29,"city":"Chicago"},
{"id":"38","name":"Elizabeth","age":32,"city":"Phoenix"},
{"id":"39","name":"Jacob","age":28,"city":"Austin"},
{"id":"40","name":"Samantha","age":27,"city":"San Jose"},
{"id":"41","name":"Matthew","age":26,"city":"San Diego"},
{"id":"42","name":"Ashley","age":31,"city":"San Francisco"},
{"id":"43","name":"Joshua","age":30,"city":"Seattle"},
{"id":"44","name":"Olivia","age":29,"city":"Houston"},
{"id":"45","name":"Daniel","age":32,"city":"Dallas"},
{"id":"46","name":"Emma","age":28,"city":"Miami"},
{"id":"47","name":"William","age":27,"city":"Boston"},
{"id":"48","name":"Sophia","age":26,"city":"Philadelphia"},
{"id":"49","name":"Joseph","age":31,"city":"Atlanta"},
{"id":"50","name":"Mia","age":30,"city":"San Antonio"}
]


class BaseAgent:
    BASE = """{DESC}
{EXAMPLE}
{OUTPUT_FORMAT}
{DATA}
"""
    def __init__(self, *point, target="", format=""):
        self._example = ""
        self._point = point
        self._target = target
        self._output_format = format
        self._data = []
        self._data_title = "# fowllow is data:"
        self._example_title = "# example:"
        self._output_format_title = "# output use this format:"
    
    @property
    def description(self):
        base = f"# {self.desc}:\n" 
        for no,i in enumerate(self.point):
            base += f" {no+1}. {i}.\n"
        return base
    
    @property
    def example(self):
        return self._example
    @property
    def output_format(self):
        return self._output_format
    @property
    def point(self):
        return self._point
    @property
    def desc(self):
        return self._target
    
    def input(self, *items):
        self._data = items
        return self
    
    def __truediv__(self, data):
        if isinstance(data, str):
            return self.input(data)
        elif isinstance(data, Iterable):
            return self.input(*data)
        else:
            raise ValueError("data must be string or iterable")

    def update(self, agent):
        if agent._example:
            self._example = agent._example
        
        if agent._output_format:
            self._output_format = agent._output_format
        
        if agent._target:
            self._target = agent._target
        
        if agent._point and len(agent._point) > 0:
            self._point = agent._point

        if agent._data and len(agent._data) > 0:
            self._data = agent._data
        
        if agent._data_title:
            self._data_title = agent._data_title
        
        if agent._output_format_title:
            self._output_format_title = agent._output_format_title
        
        if agent._example_title:
            self._example_title = agent._example_title

        return self
    
    def data_batch(self, batch_size=20):
        data = []
        for i in self._data:
            data.append(i)
            if len(data) == batch_size:
                yield data
                data = []
        if len(data) > 0:
            yield data


    def __str__(self):
        data = "\n\n".join([convertstr(i) for i in next(self.data_batch(batch_size=5))])
        if data.strip() != "":
            data = self._data_title +"........" +"\n"+ data
        
        _example = self.example
        if _example != "":
            _example = self._example_title +"\n"+ self._example

        _output_format = self.output_format
        if self._output_format != "":
            _output_format = self._output_format_title +"\n"+ self.output_format
        
        return self.BASE.format(DESC=self.description, EXAMPLE=_example, OUTPUT_FORMAT=_output_format, DATA=data).strip()
    
    def output(self, batch_size=10):
        for items in self.data_batch(batch_size):
            data = "\n\n".join([convertstr(i) for i in items])
            if data.strip() != "":
                data = self._data_title +"\n"+ data
            
            _example = self.example
            if _example != "":
                _example = self._example_title +"\n"+ self._example

            _output_format = self.output_format
            if self._output_format != "":
                _output_format = self._output_format_title +"\n"+ self.output_format
            
            yield self.BASE.format(DESC=self.description, EXAMPLE=_example, OUTPUT_FORMAT=_output_format, DATA=data).strip()

    def __repr__(self):
        return self.__str__()

class Agent(BaseAgent):
    def __rshift__(self, other):
        if isinstance(other, BaseAgent):
            return other.update(self)
        elif isinstance(other, type):
            other_instance = other()
            return other_instance.update(self)
        else:
            raise TypeError("Right operand must be an instance of BaseAgent or a subclass of BaseAgent")
    
    def output_to_llm(self, llm, batch_size=10, datas=[]):
        if len(datas) > 0:
            for o in datas:
                strIO = StringIO()
                llm.out(o, out=strIO)
                strIO.seek(0)
                yield strIO.read()
        else:
            for o in self.output(batch_size=batch_size):
                strIO = StringIO()
                llm.out(o, out=strIO)
                strIO.seek(0)
                yield strIO.read()

    def __add__(self, llm):
        return self.output_to_llm(llm)

class JsonAgent(Agent):
    argu:str = "chooses"
    key:str = "id"
    def __init__(self, *point,key="id",type="choose", target="", format="use this format to output: "):
        super().__init__(*point, target=target, format=format)
        self.key = key
        self.argu = type

    @property
    def output_format(self):
        if self._data is None or len(self._data) == 0:
            return ""
        base = ""
        if self.key in self._data[0]:
            if self.argu == "choose" or self.argu == "select" or self.argu == "pick" or self.argu == "choose one":
                base = '{'+f'"{self.key}": "here is your {self.key}"'+'} , ps: only can output one item'
            elif self.argu == "chooses" or self.argu == "selects" or self.argu == "picks" or self.argu == "choose all":
                base = f'[%s"{self.key}": "here is your {self.key}"%s, %s"{self.key}": "here is another item\'s {self.key}"%s....]' % ("{" , "}", "{", "}")
        return self._output_format + base + "\n"
    
    def output_to_llm(self, llm, batch_size=10):
        erros = []
        for output in super().output_to_llm(llm, batch_size):
            try:
                item_str = output.split("```json")[1].split("```")[0]
                yield json.loads(item_str)
            except Exception as e:
                try:
                    item_str = output.split("```json")[1].split("```")[0]
                except Exception as e:
                    logger.error(str(e) + "  >> "+output)
                    erros.append(output)
        if len(erros) > 0:
            for e in super().output_to_llm(llm, batch_size, datas=erros):
                try:
                    item_str = e.split("```json")[1].split("```")[0]
                    yield json.loads(item_str)
                except Exception as e:
                    try:
                        item_str = output.split("```json")[1].split("```")[0]
                    except Exception as e:
                        logger.error(str(e) + "  >> "+output)
                        erros.append(output)
