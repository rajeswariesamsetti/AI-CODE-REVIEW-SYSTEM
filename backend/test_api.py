import json
import requests

def test():
    print("Testing Python Execution...")
    try:
        r = requests.post("http://127.0.0.1:5000/run", json={"code": "name=input('Name: ')\nprint(f'Hello {name}')", "language": "python", "stdin": "Alice"})
        print(json.dumps(r.json(), indent=2))
        
        print("\nTesting JS Execution...")
        r = requests.post("http://127.0.0.1:5000/run", json={"code": "console.log('JS execution test')", "language": "javascript", "stdin": ""})
        print(json.dumps(r.json(), indent=2))

        print("\nTesting Python Review...")
        r = requests.post("http://127.0.0.1:5000/review", json={"code": "a = 5\nb = 10\nprint(a+b)", "language": "python"})
        print(json.dumps(r.json(), indent=2))
        
        print("\nTesting JS Review...")
        r = requests.post("http://127.0.0.1:5000/review", json={"code": "eval('2+2'); console.log('test')", "language": "javascript"})
        print(json.dumps(r.json(), indent=2))
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    test()
