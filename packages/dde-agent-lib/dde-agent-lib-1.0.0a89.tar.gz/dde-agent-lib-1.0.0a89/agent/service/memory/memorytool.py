import json
from urllib.parse import unquote

from agent.fegin.portal_client import PortalClient
from agent.utils.dde_logger import format_log


class MemoryService:
    def __init__(self, logger, portal_address, system_config):
        self.logger = logger
        self.portal_client = PortalClient(logger, portal_address, system_config)

    # 检查当前轮对话是否上传pdf文档
    def check_last_contain_pdf(self, data):
        second_last_element = data[-2]
        if 'resourceList' in second_last_element:
            resource_list = second_last_element['resourceList']
            if resource_list:
                for item in resource_list:
                    if '.pdf' in item.lower():
                        return True
        return False

    # 获取history中最后一个pdf文档的index
    def find_last_pdf_order_index(self, data):
        # 查找包含 PDF 类型的最后一个文档的 orderIndex
        last_pdf_order_index = None
        for message in reversed(data):
            if 'resourceList' in message and message['resourceList']:
                for resource in message['resourceList']:
                    if '.pdf' in resource.lower():
                        last_pdf_order_index = message['orderIndex']
                        break
            if last_pdf_order_index:
                break
        return last_pdf_order_index

    # 获取完整的memory信息，包括所使用的工具
    def retrieve_complete_memory(self, session_id: str, max_round: int = 20, max_length: int = 4000, remove_current_chat: bool = True):
        self.logger.info(f'根据session_id[%s]从portal后端查询retrieve_complete_memory', session_id)
        memories = []
        try:
            memory_resp = self.portal_client.get_chat_detail(session_id)
            if memory_resp is None or memory_resp.get("data") is None or memory_resp.get("data").get("conversation") is None:
                self.logger.info(f'根据session_id[%s]从portal后端查询历史消息为空，请检查参数', session_id)
                self.logger.info(f'retrieve_memory,session_id[{session_id}],return[]')
                return []
            chat_info_list = memory_resp.get('data').get('conversation')
            self.logger.info(f'根据session_id[{session_id}]从portal后端查询retrieve_complete_memory, chat_info_list:{json.dumps(chat_info_list)}')
            if len(chat_info_list) < 2:
                self.logger.info(f"retrieve_complete_memory,len(chat_info_list) < 2, return[],session_id={session_id}")
                self.logger.info(f'retrieve_complete_memory,session_id[{session_id}],return[]')
                return []
            if remove_current_chat:
                chat_info_list = chat_info_list[:-2]
                self.logger.info(f'session_id[{session_id}], remove_current_chat is true, remove last 2 chat_info')
            memory_length = 0
            memory_round = 0
            for i in range(len(chat_info_list) - 1, -1, -2):
                if max_round > 0 and memory_round >= max_round:
                    self.logger.info(f'当前历史对话轮数超过{max_round}轮,不再新增历史对话,session_id[{session_id}]')
                    break
                chat_memory = {}
                if chat_info_list[i - 1]['text'] is None or chat_info_list[i]['text'] is None:
                    continue
                chat = chat_info_list[i - 1]["text"]
                chat = chat.replace("\\n", "\n")
                chat_memory.update({"question": chat, "chatId": chat_info_list[i - 1]["chatId"]})
                files = []
                if len(chat_info_list[i - 1]["resourceList"]) > 0:
                    for resource in chat_info_list[i - 1]["resourceList"]:
                        data = json.loads(resource)
                        files.append(data['url'])
                chat_memory.update({'files': files})
                plugin = chat_info_list[i]["pluginCode"]
                if plugin == 'Code Agent':
                   continue
                is_reference = True
                if "Web Search" in plugin:
                    is_reference = False
                content = self.retrieve_content_from_answer(chat_info_list[i]['text'], is_reference)
                content = content.replace("\\n", "\n")
                chat_memory.update({"answer": content})
                chat_memory.update({"plugin": plugin})
                memory_length = memory_length + len(json.dumps(chat_memory))
                if max_length > 0 and memory_length >= max_length:
                    self.logger.info(f'当前历史对话字符长度超过{max_length},不再新增历史对话,session_id[{session_id}]')
                    break
                memories.insert(0, chat_memory)
                memory_round = memory_round + 1
        except Exception as e:
            self.logger.error("获取历史消息时，发生%s异常", str(e), exc_info=True)
        self.logger.info(f'retrieve_complete_memory,session_id[{session_id}],return[{memories}]')
        return memories

    def retrieve_complete_memory_question(self, session_id: str, max_round: int = 20, max_length: int = 5000, remove_current_chat: bool = True):
        self.logger.info(f'根据session_id[{session_id}]从portal后端查询历史记录中的问题部分 retrieve_complete_memory_question')
        memories = []
        try:
            memory_resp = self.portal_client.get_chat_detail(session_id)
            if memory_resp is None or memory_resp.get("data") is None or memory_resp.get("data").get("conversation") is None:
                self.logger.info(f'根据session_id[%s]从portal后端查询历史记录中的问题部分,返回数据为空,请检查参数', session_id)
                self.logger.info(f'retrieve_complete_memory_question,session_id[{session_id}],return[]')
                return []
            chat_info_list = memory_resp.get('data').get('conversation')
            self.logger.info(f'根据session_id[{session_id}]从portal后端查询历史记录中的问题部分 retrieve_complete_memory_question, chat_info_list:{json.dumps(chat_info_list)}')
            if len(chat_info_list) < 2:
                self.logger.info(f"retrieve_complete_memory_question,len(chat_info_list) < 2, return[],session_id={session_id}")
                self.logger.info(f'retrieve_complete_memory_question,session_id[{session_id}],return[]')
                return []
            if remove_current_chat:
                chat_info_list = chat_info_list[:-2]
                self.logger.info(f'session_id[{session_id}],retrieve_complete_memory_question, remove_current_chat is true, remove last 2 chat_info')
            memory_length = 0
            memory_round = 0
            for i in range(len(chat_info_list) - 1, -1, -2):
                if max_round > 0 and memory_round >= max_round:
                    self.logger.info(f'retrieve_complete_memory_question,当前历史对话轮数超过{max_round}轮,不再新增历史对话,session_id[{session_id}]')
                    break
                chat_memory = {}
                if chat_info_list[i - 1]['text'] is None or chat_info_list[i]['text'] is None:
                    continue
                chat = chat_info_list[i - 1]["text"]
                chat = chat.replace("\\n", "\n")
                chat_memory.update({"question": chat, "chatId": chat_info_list[i - 1]["chatId"]})

                plugin = chat_info_list[i]["pluginCode"]
                chat_memory.update({"answer": ""})
                chat_memory.update({"plugin": plugin})
                if max_length > 0 and memory_length >= max_length:
                    self.logger.info(f'retrieve_complete_memory_question,当前历史对话字符长度超过{max_length},不再新增历史对话,session_id[{session_id}]')
                    break
                memories.insert(0, chat_memory)
                format_log(_type="00_log", content=f"检索构造retrieve_complete_memory_question,当前轮次[{str(memory_round)}]的长度为[{str(memory_length)}],当前轮次的chat_memory为[{str(chat_memory)}],总的memories为[{str(memories)}]")
                memory_round = memory_round + 1
        except Exception as e:
            self.logger.error("retrieve_complete_memory_question,获取历史消息时，发生%s异常", str(e), exc_info=True)
        self.logger.info(f'retrieve_complete_memory_question,session_id[{session_id}],return[{memories}]')
        return memories

    def retrieve_memory(self, session_id: str, split_pdf: bool = False):
        self.logger.info(f'根据session_id[%s]从portal后端查询历史消息, split_pdf=[%s]', session_id, split_pdf)
        memories = []
        try:
            memory_resp = self.portal_client.get_chat_detail(session_id)
            if memory_resp is None or memory_resp.get("data") is None or memory_resp.get("data").get("conversation") is None:
                self.logger.info(f'根据session_id[%s]从portal后端查询历史消息为空，请检查参数', session_id)
                self.logger.info(f'retrieve_memory,session_id[{session_id}],return[]')
                return []
            chat_info_list = memory_resp.get('data').get('conversation')
            if len(chat_info_list) < 2:
                self.logger.info(f"retrieve_memory,len(chat_info_list) < 2, return[],session_id={session_id}")
                self.logger.info(f'retrieve_memory,session_id[{session_id}],return[]')
                return []
            # 如果本轮对话上传了pdf，则不传history
            if self.check_last_contain_pdf(chat_info_list):
                self.logger.info(f"chat contain pdf, return[],session_id={session_id}")
                self.logger.info(f'retrieve_memory,session_id[{session_id}],return[]')
                return []
            chat_info_list = chat_info_list[:-2]
            if split_pdf:
                # 对于文献解析，本轮没有上传pdf，则需要清除上一个pdf之前的history
                last_pdf_index = self.find_last_pdf_order_index(chat_info_list)
                if last_pdf_index is not None:
                    chat_info_list = chat_info_list[last_pdf_index:]
            num = 0
            memory_length = 0
            for i in range(0, len(chat_info_list), 2):
                chat_memory = []
                if chat_info_list[i]['text'] is not None and chat_info_list[i + 1]['text'] is not None:
                    chat = chat_info_list[i]["text"]
                    chat = chat.replace("\\n", "\n")
                    chat_memory.append(chat)
                    content = self.retrieve_content_from_answer(chat_info_list[i + 1]['text'])
                    content = content.replace("\\n", "\n")
                    chat_memory.append(content)
                    memories.append(chat_memory)
                num += 1
                if chat_memory is not None:
                    memory_length = memory_length + len(chat_memory)
                if num >= 20:
                    self.logger.info(f'当前历史对话轮数超过20轮,不再新增历史对话,session_id[{session_id}]')
                    break
                if memory_length >= 4000:
                    self.logger.info(f'当前历史对话字符长度超过4000,不再新增历史对话,session_id[{session_id}]')
                    break
        except Exception as e:
            self.logger.error("获取历史消息时，发生%s异常", str(e), exc_info=True)
        self.logger.info(f'retrieve_memory,session_id[{session_id}],return[{memories}]')
        return memories

    def retrieve_content_from_answer(self, content, is_reference=True):
        '''处理历史消息中各式各样的markdown格式和json格式'''
        self.logger.info(f"retrieve_content_from_answer data:[{content}]")
        all_contents = ''
        try:
            data = json.loads(content)
            # 遍历列表，提取每个元素的content字段，并进行URL解码
            for item in data:
                content = self.handle_memory_item(item, is_reference)
                if content:
                    all_contents += content
            if len(all_contents) > 20000:
                all_contents = all_contents[:20000]
        except Exception as e:
            self.logger.error("加载历史消息时，发生%s异常", str(e), exc_info=True)
        return all_contents

    def handle_memory_item(self, item, is_reference):
        '''
          依次处理历史消息中各式各样的格式，包括MarkDown Data_Visualization AcademicList等
        '''
        content = None
        try:
            if 'MarkDown' == unquote(item['type']) or 'MarkDownTable' == unquote(item['type']):
                content = unquote(item['content'])
                content = content.replace('<div style="display:flex;flex-wrap:wrap;"><span style="margin-top: 2px; margin-right: 8px">','').replace('</span><font style="background-color:rgba(28, 113, 230, 0.14); padding-top: 2px; padding-bottom: 2px; padding-left: 10px; padding-right: 10px; margin-right: 8px; border-radius: 6px; margin-bottom: 2px">','').replace('</font><span style="margin-top: 2px">', '').replace('</span></div>', '')
            if 'Data_Visualization' == unquote(item['type']) or 'AcademicList' == unquote(item['type']):
                content = json.dumps(item['content'])
            if 'Reference' == unquote(item['type']) and is_reference:
                content = json.dumps(item['content'])
            if 'AcademicList' == unquote(item['type']):
                academic_list_content = item['content']
                number = 1
                for academic_list_content_item in academic_list_content:
                    academic_list_content_item_str = self.academic_list_content_item_construction(number, str(academic_list_content_item))
                    content = content + academic_list_content_item_str + "\n"
            if 'MarkDownCode' == unquote(item['type']):
                if item['subType'] == "runCode":
                    content = unquote(item["content"]["result"])
                elif item['subType'] == "showCode":
                    content = f'```{item["content"]["codeType"]}{unquote(item["content"]["content"])}```'
            if content and len(content) > 10000:
                content = content[:10000]
        except Exception as e:
            self.logger.error("加载历史消息时，发生%s异常", str(e), exc_info=True)
            self.logger.error(e)
        return content
    def academic_list_content_item_construction(self, number, academic_list_item):
        '''
          根据AcademicList中content拼接其中的item，拼接其中的每个对象
          {"type": "AcademicList", "content": [{"id": 1, "tag": "journal", "items": [{"text": "Nuclear magnetic resonance response characteristics and quantitative evaluation method of fluid saturation of lacustrine shale oil:", "url": "https://www.semanticscholar.org/paper/81c1a8e959a45496435ebc805342de8e354a9070"}, {"text": "The quantitative evaluation of fluid saturation is important for formation evaluation of shale oil. However, there is currently no effective method to identify the fluid occurrence state and quantitative evaluate the fluid saturation of lacustrine shale oil because of the complexity of diagenetic minerals and pore types. In this paper, a method is proposed for the quantitative evaluation of fluid saturation based on nuclear magnetic resonance (NMR), X-ray diffraction (XRD) and scanning electron ... "}, {"text": "Ruiqi Fan, G. Liao, Rui Mao, Xing-ping Luo, L. Hou, Hao Zhang, Hua Tian, G. Wang, Zhijun Qin, Lizhi Xiao"}, {"text": " —— <<Frontiers in Earth Science>>"}, {"text": " u2014u2014 2023"}]}]}
        '''
        academic_list_item_str = ''
        try:
            academic_list_content = json.loads(academic_list_item)
            for item in academic_list_content['content']:
                # 获取标题
                title = item['items'][0]['text']
                # 获取摘要
                abstract = item['items'][1]['text']
                # 获取作者
                authors = item['items'][2]['text']
                # 获取期刊名称
                journal = item['items'][3]['text']
                # 获取年份
                year = item['items'][4]['text']
                academic_list_item_str = f"{number} {title}: {abstract} {authors}{journal}{year}"


        except Exception as e:
            self.logger.error(f'学术搜索中,根据AcademicList中content拼接其中的item[{academic_list_item}]出现异常[{str(e)}]')
            self.logger.error(e)
        return academic_list_item_str

