from unicodedata import normalize
import alkana
import MeCab
import ipadic
from pykakasi import kakasi
import re
from pprint import pprint

m = MeCab.Tagger(ipadic.MECAB_ARGS) #mecabのtagger objectの宣言


class Hatsuon:
	def __init__(self) -> None:
		self.kakasi = kakasi()

	def unify(self, sentence):
		to_upper = sentence.upper()
		to_normalize = normalize('NFKC', to_upper)
		return to_normalize

	def word_replace(self, sentence):
		sentence.replace("は", "わ")
		word = [x for x in sentence.split()]

		for x in word:
			yomi = alkana.get_kana(x)
			if yomi is not None:
				#yomi = yomi[:1] + "'" + yomi[1:]
				sentence = sentence.replace(x, yomi)

		return sentence

	def bunsetsuWakachi(self, text):
		# 以下のコードをお借りしました。
		# https://qiita.com/shimajiroxyz/items/e44058af8b036f5354aa
		m_result = m.parse(text).splitlines()
		m_result = m_result[:-1] #最後の1行は不要な行なので除く
		break_pos = ['名詞','動詞','接頭詞','副詞','感動詞','形容詞','形容動詞','連体詞'] #文節の切れ目を検出するための品詞リスト
		wakachi = [''] #分かち書きのリスト
		afterPrepos = False #接頭詞の直後かどうかのフラグ
		afterSahenNoun = False #サ変接続名詞の直後かどうかのフラグ
		for v in m_result:
			if '\t' not in v: continue
			surface = v.split('\t')[0] #表層系
			pos = v.split('\t')[1].split(',') #品詞など
			pos_detail = ','.join(pos[1:4]) #品詞細分類（各要素の内部がさらに'/'で区切られていることがあるので、','でjoinして、inで判定する)
			#この単語が文節の切れ目とならないかどうかの判定
			noBreak = pos[0] not in break_pos
			noBreak = noBreak or '接尾' in pos_detail
			noBreak = noBreak or (pos[0]=='動詞' and 'サ変接続' in pos_detail)
			noBreak = noBreak or '非自立' in pos_detail #非自立な名詞、動詞を文節の切れ目としたい場合はこの行をコメントアウトする
			noBreak = noBreak or afterPrepos
			noBreak = noBreak or (afterSahenNoun and pos[0]=='動詞' and pos[4]=='サ変・スル')
			if noBreak == False:
				wakachi.append("")
			wakachi[-1] += surface
			afterPrepos = pos[0]=='接頭詞'
			afterSahenNoun = 'サ変接続' in pos_detail
		if wakachi[0] == '': wakachi = wakachi[1:] #最初が空文字のとき削除する
		return wakachi

	def kanji_reverse_conv(self, word):
		result = []
		for x in word:
			raw = self.kakasi.convert(x)
			hira = [y['hira'] for y in raw]
			result.append("".join(hira))

		return "/".join(result)

	def number(self, sentence):
		pattern = r"\d+"
		matches = re.findall(pattern, sentence)
		for match in matches:
			sentence = sentence.replace(match, f"<NUMK VAL={match}>")
		return sentence

	def convert(self, sentence):
		unified = self.unify(sentence)
		replaced = self.unify(self.word_replace(unified))
		bunsetu = self.bunsetsuWakachi(replaced)
		kanji = self.kanji_reverse_conv(bunsetu)
		result = self.number(kanji)
		return result

if __name__ == "__main__":
	hatsuon = Hatsuon()
	sentence = "Hello World こんにちは4人の皆さん。"
	unified = hatsuon.unify(sentence)
	print("統合: "+unified)
	replaced = hatsuon.unify(hatsuon.word_replace(unified))
	print("置き換え: "+replaced)
	bunsetu = hatsuon.bunsetsuWakachi(replaced)
	print("分節: "+ str(bunsetu))
	kanji = hatsuon.kanji_reverse_conv(bunsetu)
	print("漢字変換: "+kanji)
	number = hatsuon.number(kanji)
	print("数字変換: "+number)