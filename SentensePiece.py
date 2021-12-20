def read_text(textfile):
    with open(textfile, encoding="utf-8_sig") as f:
        corpus = f.read()
    return corpus


def preprocessing(corpus, user_name):
    remarks = [sentence.split("\t") for sentence in corpus.split(
        "\n") if len(sentence.split("\t")) == 3]
    sentences = [remark[2] for remark in remarks if remark[1] == user_name]
    return sentences


def make_file_name(person_name, text_file):
    person = person_name.replace(' ', '_')
    new_file = person + text_file
    return new_file


def split_text(sentence, sp):

    sp_list = []
    fin = '\n'

    # 単語ごとに分割したテキストをリストに格納
    for s in sentence:
        temp = sp.EncodeAsPieces(s)
        temp.append(fin)
        sp_list.append(temp)

    return sp_list


def make_2states_model(sp_list):
    model = {}
    for sentence in sp_list:
        word0 = 'BoS0'  # begin of sentence
        word1 = 'BoS1'
        # del_mark = '_'
        for word in sentence:
            # if word in del_mark:
            if word == '_':
                break
            key = (word0, word1)
            if key in model:
                model[key].append(word)
            else:
                model[key] = [word]
            word0, word1 = word1, word
    return model


def generate_sentence2(model):
    from random import randint

    eos_mark = '\n'
    key0_list = model[('BoS0', 'BoS1')]
    key0 = key0_list[randint(0, len(key0_list) - 1)]
    key1_list = model[('BoS1', key0)]
    key1 = key1_list[randint(0, len(key1_list) - 1)]
    result = key0 + key1

    while key1 not in eos_mark:
        key_list = model[(key0, key1)]
        key = key_list[randint(0, len(key_list) - 1)]
        result += key
        key0, key1 = key1, key
    return result


def reply():
    import codecs
    import sentencepiece as spm
    import os

    text_file = 'lineTalk.txt'
    person_name = '渡邉 渉'

    coupus = read_text(text_file)
    sentence = preprocessing(coupus, person_name)

    dir_name = "text_file"

    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    new_text_file = make_file_name(dir_name + "/" + person_name, text_file)

    print(*sentence, sep="\n", file=codecs.open(new_text_file, "w", "utf-8"))

    # 学習の実行
    spm.SentencePieceTrainer.Train(
        '--input=' +
        new_text_file +
        ' --model_prefix=sentencepiece --vocab_size=4000 --character_coverage=0.9995 --pad_id=3')

    # モデルの作成
    sp = spm.SentencePieceProcessor()
    sp.Load("sentencepiece.model")

    sp_list = split_text(sentence, sp)

    model = make_2states_model(sp_list)

    generate = generate_sentence2(model)

    reply_text = generate[1:].replace('\n', '')

    return reply_text


# if __name__ == '__main__':
#     main()
