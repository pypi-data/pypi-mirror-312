from funasr import AutoModel

def main():
    model = AutoModel(model="ct-punc")

    res = model.generate(input="那今天的会就到这里吧 happy new year 明年见")
    print(res)

if __name__ == '__main__':
    main()