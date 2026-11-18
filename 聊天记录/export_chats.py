import json, re, os
from datetime import datetime, timezone, timedelta

SRC='/home/hatch/agents/agent-905392cb-0a4d-4fed-a6e5-03f4f582e854/sessions/905392cb-0a4d-4fed-a6e5-03f4f582e854.jsonl'
OUTDIR='/tmp/chat-export'
CST=timezone(timedelta(hours=8))
CHAT_ID='5716ec88-2d92-4cd6-9835-69b5fb149e02'

def parse_ts(s):
    if not s: return None
    s=re.sub(r'(\.\d{6})\d+', r'\1', str(s))
    try: return datetime.fromisoformat(s.replace('Z','+00:00'))
    except Exception: return None

def fmt_ts(dt):
    return dt.astimezone(CST).strftime('%Y-%m-%d %H:%M:%S') if dt else '时间未知'

msgs=[]; fallback=0; attach_notes=0
with open(SRC,encoding='utf-8') as f:
    for line in f:
        o=json.loads(line)
        if o.get('type')!='item': continue
        it=o.get('item') or {}
        k=it.get('type'); role=it.get('role'); src=o.get('source')
        dt=parse_ts(o.get('created_at'))
        if k=='message':
            t=it.get('text')
            if t is None: t=''
            if not isinstance(t,str):
                t=json.dumps(t,ensure_ascii=False); fallback+=1
            msgs.append((o.get('seq'),dt,role,src,t))
        elif k=='message_parts':
            chunks=[]
            for part in (it.get('parts') or []):
                if not isinstance(part,dict): continue
                pt=part.get('type')
                if pt=='text':
                    chunks.append(part.get('text') or '')
                elif pt=='file_ref':
                    attach_notes+=1
                    note='[附件：%s（%s，%s 字节）]'%(part.get('filename'),part.get('mime_type'),part.get('bytes_len'))
                    if part.get('transcription'):
                        note+='\n[语音转写] '+str(part['transcription'])
                    chunks.append(note)
                else:
                    chunks.append('[附件：类型 %s]'%pt)
            msgs.append((o.get('seq'),dt,role,src,'\n\n'.join(chunks)))

msgs.sort(key=lambda x: x[0] or 0)
import collections
byrole=collections.Counter(m[2] for m in msgs)
total_chars=sum(len(m[4]) for m in msgs)
dts=[m[1] for m in msgs if m[1]]
dmin,dmax=min(dts),max(dts)
fname='%s至%s-主聊天.md'%(dmin.astimezone(CST).strftime('%Y-%m-%d'), dmax.astimezone(CST).strftime('%Y-%m-%d'))
label={'user':'用户','assistant':'Muse','developer':'系统移交'}
out=os.path.join(OUTDIR,fname)
with open(out,'w',encoding='utf-8') as w:
    w.write('# 聊天记录导出：主聊天\n\n')
    w.write('- 聊天标题：主聊天（系统 thread_title：打开抖音创作者中心）\n')
    w.write('- chat_id：%s\n'%CHAT_ID)
    w.write('- 消息总数：%d（用户 %d／Muse %d／系统移交 %d）\n'%(len(msgs),byrole['user'],byrole['assistant'],byrole['developer']))
    w.write('- 时间范围：%s 至 %s（Asia/Shanghai）\n'%(fmt_ts(dmin),fmt_ts(dmax)))
    w.write('- 导出日期：2026-11-18\n')
    w.write('- 数据来源：主 agent 本地会话 transcript 文件（~/agents/agent-905392cb-0a4d-4fed-a6e5-03f4f582e854/sessions/905392cb-0a4d-4fed-a6e5-03f4f582e854.jsonl），按 seq 顺序导出其中的 message / message_parts 条目；thinking、工具调用与工具输出、压缩检查点不属于聊天消息，未纳入。\n')
    w.write('- 附件仅记录文件名与类型，不嵌二进制；语音附件附转写文本。\n')
    w.write('\n---\n')
    for seq,dt,role,src,text in msgs:
        lab=label.get(role,role or '未知')
        if role=='developer': lab='系统移交（来源：%s）'%src
        w.write('\n### %s · %s\n\n%s\n'%(fmt_ts(dt),lab,text))
print(json.dumps({'file':out,'messages':len(msgs),'byrole':dict(byrole),'total_chars':total_chars,
 'range':[fmt_ts(dmin),fmt_ts(dmax)],'fallback':fallback,'attachments':attach_notes,
 'bytes':os.path.getsize(out)},ensure_ascii=False))
