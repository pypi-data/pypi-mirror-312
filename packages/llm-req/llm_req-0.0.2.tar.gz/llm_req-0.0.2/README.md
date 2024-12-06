
# llm_req

<code>auth</code>

> https://github.com/xxx

chatglm-llm client


## usage

```python
from llm_req import LLM, Voice

# normal
llm = LLM(remote_host=xxx.x.x.x.x)

for i in llm("nihao"):
    # i is {"new":"xxx", "response":"all....."}
    print(i["new"], end="", flush=True)

# 直接流式输出
llm << "nihao"

# use tools
llm = LLM(remote_host=xxx.x.x.x.x, use_tools=True)
llm("今天的天气")
```

### 语音功能

```python
# 使用语音包
voice = Voice(remote_host=xxx.x.x.x.x)

# 语音识别转文字
res = voice.v2t("/xxx.x.x.x/xxx.wav")
print(res.data[0]["text"])

# 文本转语音
voice.t2v("一些对话 。。。。。") # generator 
for audio_file in voice.t2v_file("一些对话 。。。。。",  "/tmp"):
    # 播放语音
    # 这里用pyaudio
    voice.play(audio_file)


```

## tools

## 使用函数回调

```python
from llm_req import LLM, Voice, get_tools
llm = LLM(remote_host=xxx.x.x.x.x, use_tools=True)
llm.functions = get_tools()
llm("今天的天气")
```

### 怎么新加tools

```python
from llm_req import LLM, Voice, get_tools
from typing import  Annotated

@as_tool
def get_weather(
    city_name: Annotated[str, 'The name of the city to be queried', True],
    ) -> str:
    """
    Get the current weather for `city_name`
    """

    if not isinstance(city_name, str):
        raise TypeError("City name must be a string")

    key_selection = {
        "current_condition": ["temp_C", "FeelsLikeC", "humidity", "weatherDesc",  "observation_time"],
    }
    import requests
    try:
        resp = requests.get(f"https://wttr.in/{city_name}?format=j1")
        resp.raise_for_status()
        resp = resp.json()
        ret = {k: {_v: resp[k][0][_v] for _v in v} for k, v in key_selection.items()}
    except:
        import traceback
        ret = "Error encountered while fetching weather data!\n" + traceback.format_exc() 

    return str(ret)

@as_tool
def get_loc(
    ip_address: Annotated[str, 'The IP address. if set None will use current machine\'s ip', False] = None,
    ) -> dict:
    """
    通过ip获取当前的地理位置信息
    """
    import requests
    import bs4
    if ip_address == None:
        res = requests.get("http://cip.cc").text
        rr = {}
        for l in res.strip().split("\n"):
            if ":" in l:
                fs = l.split(":")
                rr[fs[0].strip()] = fs[1].strip()
    else:
        res = requests.get("http://cip.cc/"+ip_address).text
        res = bs4.BeautifulSoup(res, 'html.parser').text
        rr = {}
        for l in res.strip().split("\n"):
            if ":" in l:
                fs = l.split(":")
                rr[fs[0].strip()] = fs[1].strip()
    return rr

@as_tool
def speaker(
    msg: Annotated[str, 'The message to be spoken.', True],
    ):
    """
    调用本地的语音库播放 msg
    """
    import tempfile
    from llm_req import Voice
    v = Voice(remote_host="115.236.8.146")
    tmp = tempfile.mkdtemp()
    
    for f in v.t2v_file(msg, tmp):
        v.play(f)
    return "执行完毕"
```
