P=Exception
H='title'
G=dict
F=isinstance
B=''
A=print
import os,json,requests as M,xmltodict as N
from datetime import datetime as c
C='https://www.data.jma.go.jp/developer/xml/feed/eqvol.xml'
E='nearly-earthquake.json'
O={'1':1.,'2':2.,'3':3.,'4':4.,'5弱':5.,'5強':5.5,'6弱':6.,'6強':6.5,'7':7.}
def Q():
	try:B=M.get(C,timeout=10);B.raise_for_status();return N.parse(B.text)
	except P as D:A(f"フィードの取得に失敗しました: {D}");return
def R(xml_url):
	b='Head';a='Name';Z='Area';Y='MaxInt';X='Observation';Q=xml_url;L='Report'
	try:
		R=M.get(Q,timeout=10);R.raise_for_status();I=N.parse(R.text);S=I.get(L,{}).get('Body',{});J=S.get('Intensity',{})
		if not J:return
		C=J.get(X,{}).get(Y,B)
		if not C or O.get(C,0)<3.:A(f"最大震度 {C} のため対象外です。");return
		D=J.get(X,{}).get('Pref',[])
		if F(D,G):D=[D]
		T=[]
		for d in D:
			E=d.get(Z,[])
			if F(E,G):E=[E]
			for U in E:
				e=U.get(a);K=U.get(Y)
				if K and O.get(K,0)>=3.:T.append({'area':e,'intensity':K})
		V=S.get('Earthquake',{});W=V.get('OriginTime',B);f=V.get('Hypocenter',{}).get(Z,{}).get(a,'不明');g={H:I.get(L,{}).get(b,{}).get('Title',B),'datetime':W if W else I.get(L,{}).get(b,{}).get('ReportDateTime',B),'hypocenter':f,'max_intensity':C,'regions':T,'updated_at':c.utcnow().isoformat()+'Z'};return g
	except P as h:A(f"個別XMLの解析に失敗しました ({Q}): {h}");return
def D():
	I=Q()
	if not I:return
	C=I.get('feed',{}).get('entry',[])
	if F(C,G):C=[C]
	D=None
	for J in C:
		K=J.get(H,B)
		if'震度速報'in K or'震源・震度に関する情報'in K:D=J;break
	if not D:A('直近10分以内に配信された対象の地震情報はありません。');return
	L=D.get('id');A(f"最新の地震情報を解析中: {D.get(H)} ({L})");M=R(L)
	if M:
		with open(E,'w',encoding='utf-8')as N:json.dump(M,N,ensure_ascii=False,indent=2)
		A(f"震度3以上の地震情報を {E} に保存しました。")
	else:A('保存条件（震度3以上）を満たすデータがありませんでした。')
if __name__=='__main__':D()
