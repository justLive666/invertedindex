import pytest
import invertedindex


def test_can_use_pytest_1():
    assert pytest


def test_can_import_inverted_index_2():
    assert invertedindex


def test_can_use_function_stop_words_3(tmpdir):
    tfile = tmpdir.join('test_temp_file_stop_words')
    tfile.write('a\ndd\nssa\nsfd')
    test_stop_words = invertedindex.load_stop_words(filepath=tfile)
    etalon = ['a', 'dd', 'ssa', 'sfd']
    assert etalon == test_stop_words


def test_use_temp_file_of_stop_words_4(tmpdir):
    tfile = tmpdir.join('test_temp_file_stop_words')
    tfile.write('\nhe\ni\nshe\nthe\n')
    test_stop_words = invertedindex.load_stop_words(filepath=tfile)
    etalon = ['he', 'i', 'she', 'the']
    assert etalon == test_stop_words


def test_use_temp_file_of_stop_words_5(tmpdir):
    tfile = tmpdir.join('test_temp_file_stop_words')
    tfile.write('\n12\ndd\nsss\nthe')
    test_stop_words = invertedindex.load_stop_words(filepath=tfile)
    etalon = ['12', 'dd', 'sss', 'the']
    assert etalon == test_stop_words


# load documents

def test_use_temp_file_of_load_documents_1(tmpdir):
    tfile = tmpdir.join('test_temp_file_load_documents')
    tfile.write('1\ttwo one hello\n2\tb one\n')
    test_load_document = invertedindex.load_documents(filepath=tfile)
    etalon_words = [['two', 'one', 'hello'], ['b', 'one']]
    etalon_index = [1, 2]
    assert etalon_words == test_load_document[0]
    assert etalon_index == test_load_document[1]


def test_use_temp_file_of_clear_stop_words_1(tmpdir):
    tfile = tmpdir.join('test_temp_file_document')
    tfile.write('1\ttwo....64 one2 6hello\n2\tb- one,\n')
    sfile = tmpdir.join('test_temp_file_clear_stop_words')
    sfile.write('the\na\nan\nshe\nhello')
    test_clear_stop_words = invertedindex.clear_stop_words(invertedindex.load_documents(tfile),
                                                           invertedindex.load_stop_words(sfile))
    etalon_words = [['two', 'one'], ['b', 'one']]
    assert etalon_words == test_clear_stop_words[0]
    assert [1, 2] == test_clear_stop_words[1]


# make json
def test_make_json(tmpdir):
    tfile = tmpdir.join('test_temp_file_document')
    tfile.write('1\ttwo....64 one2 6hello\n4\tb- one,\n')
    sfile = tmpdir.join('test_temp_file_clear_stop_words')
    sfile.write('the\na\nan\nshe\nhello')
    test_clear_stop_words = invertedindex.build_inverted_index(tfile, sfile).inverted_index
    etalon_words = {
        "two": [1],
        "one": [1, 4],
        "b": [4]
    }
    assert etalon_words == test_clear_stop_words


# test query words
def test_query_words(tmpdir):
    tfile = tmpdir.join('test_temp_file_document')
    tfile.write('1\ttwo....64 one2 6hello\n4\tb- one,\n')
    sfile = tmpdir.join('test_temp_file_clear_stop_words')
    sfile.write('the\na\nan\nshe\nhello')
    words = ['two', 'one']  # two:[1] one:[1,4]
    query_crossing = invertedindex.build_inverted_index(tfile, sfile).query(words)
    print(query_crossing)
    etalon_crossing = [1]
    assert etalon_crossing == query_crossing


# test query words
def test_save_query_lines(tmpdir):
    tfile = tmpdir.join('test_temp_file_document')
    tfile.write('12\thi hello bye goodbye\n22\tone three four five hi two\n44\tgood bad two')
    sfile = tmpdir.join('test_temp_file_clear_stop_words')
    sfile.write('the\na\nan\nshe\nhello')
    outfile = '12\thi hello bye goodbye\n22\tone three four five hi two\n'
    print(outfile)
    words = ['hi']
    inverted_index = invertedindex.build_inverted_index(tfile, sfile)
    print(f"invertedindex: {inverted_index}")
    query_words = inverted_index.query(words)  # [12,22]
    print(f"query_words: {query_words}")
    query_path = r"C:\DiscD\Для учеников\mSavko\crossing.txt"
    inverted_index.save_query(tfile, query_path, words) #saving
    with open(file=query_path, encoding='utf-8', mode='r') as saved_file:
        print(saved_file.read())
        content = saved_file.read()

    assert outfile == content
