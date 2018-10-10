#encoding=utf-8

import jieba
import jieba.posseg as pseg
import re
jieba.load_userdict("User_Dict.txt")
#jieba.set_dictionary("User_Dict_With_Freq.txt")
content1 = "右额叶可见类圆形长T 2长T1信号，边界尚清，大小约28x24mm，其内可见分隔，增强扫描分隔明显强化，其 内容物无强化。双侧脑室、脑池不大，脑沟、脑裂不宽，中线结构居中.小脑及脑干形 态及信号未见明显异常。"
content2 = "左侧额叶前回及右侧额叶直回分别见大小约31x40mm及23x30mm 的团块状异常信号影，边缘模糊，T1W1呈稍低信号，T2WI呈不均匀高信号，夹杂少置稍 短T1短T2信号，增强扫描左侧额叶病灶呈花环状高强化，右侧额叶病灶呈不均匀稍高强化，局部与筛窦分界不清，病灶边缘均可见指状水肿带；左侧额叶另见一月牙形长T1长; T信号影，边界清，増强扫描未见强化，左侧脑室前角稍扩大，边界尚清。中线结构局部稍左偏，蝶鞍明显扩大，鞍内充满长T1长T2水样信号影"
content3 = "左侧顶叶可见一呈楔形长T1长T2信号，DWI呈低信号，增强后未见明显强化，其内隐约可见血管穿行。左侧脑室受压、变形、向右移位。双侧脑室前后角旁白质、半卵圆中心见点、片状稍长T1长T2信号，增强扫描未见明显强化。小脑及脑干未见明显异常。 右侧脑室及左侧侧脑室枕角、两颞角扩大，三脑室受压变窄，向右移位，第4脑室未见扩大。•桥小脑脚池增宽，脑沟、脑裂不宽，中线结构右移。蝶鞍无明显扩大，鞍内垂体信号正常。视交叉、垂体柄显示清晰。双侧海绵窦信号正常。两侧上颌窦及筛窦内粘膜增 厚"
content4 ="   双侧大脑半球结构对称。双侧放射冠、基底节区、侧脑室周围可见多发斑片状T1WI低信号、T2WI高信号、FLAIR高信号影，DWI未见明显高信号。脑室系统未见扩张，脑沟、裂未增宽，小脑及脑干未见明显异常。垂体不大。鞍上区可见一团状异常信号影，T1WI呈低信号、T2WI及T2FLAIR为稍高信号影，DWI呈稍高信号，ADC呈高信号，病灶大小约为30mm×23mm×20mm（前后×左右×上下），病灶稍压迫中脑，病灶向上压迫视交叉。"
content = content4.replace(" ","")

result = pseg.cut(content,HMM=False)
r_list = []
for w in result:
    r_list.append([w.word,w.flag])
    
# wz/jp
outp = []
slic = []
for i in range(len(r_list)):
    w = r_list[i]
    w_before = r_list[i-1]
    if w[1] in ["jp","wz","zqsm"]:
        #if w_before[1] in ["jp","wz","blgx","xhmc"]:
        if w_before[1]  not in ["x","wz"] or w_before[0]=="、":
            slic.append(w)
        else:
            outp.append(slic)
            slic = []
            slic.append(w)
    else:
        slic.append(w)
#End Slic
outp.append(slic)

print(content)
for i in outp:
    print(i)
    try:
        text = ""
        for m in i:
            text += m[0]
        seg = re.split(r",|\.|，|。", text)
        for n in seg:
            print(n)
    except:
        next
        
'''
1、根据解剖部位的描述，将描述拆分成小段落


'''