import re
import json
import aiohttp 
import requests
from requests_ip_rotator import ApiGateway
from playwright.async_api import async_playwright
from typing import Any
import asyncio
import random

"""
setattr - это настройка для aiohttp, что бы работать с прокси.
из Python3.12 без этого работать не будет.
"""
setattr(asyncio.sslproto._SSLProtocolTransport, "_start_tls_compatible", True)

class Mixin:
    async def text_normalizer(self, text: str, remove_from_str: list[str] = None) -> str:
        """
        This method takes a string as an argument and removes all occurrences of 
        the strings in the list 'defect' from the string.

        :param text: The string to be normalized
        :return: The normalized string
        """
        defect = ['\n', '\b', '\r', '\\', '\xa0', '\ufeff', '&nbsp;']
        if remove_from_str != None:
            defect.extend(remove_from_str)
        try:
            if text == None:
                return text
            for symbol in defect:
                if symbol in text:
                    text = text.replace(symbol, ' ')
                    
            return text
        except Exception as ex:
            ValueError


    async def translator(self, text: str, output_lang: str, input_lang: str = 'en') -> str:
        """
        This method takes a string as an argument and translates it from one language to another.
        It splits the string into sentences, translates each sentence using the Google Translate API,
        and then joins the translated sentences back together.

        :param text: The string to translate
        :param output_lang: The language to translate to
        :param input_lang: The language to translate from (default is 'en')
        :return: The translated string
        :raises ValueError: If an error occurs during the execution of the task
        """
        try:
            """deep_translator имеет ограничения по количеству символов за один запрос,
            поэтому мы разбиваем текст на несколько частей,
            чтобы не превышать лимит."""
            text_list = text.split('.') # Split the text into sentences
            translate_text = []
            for text in text_list:
                translate_text.append(GoogleTranslator(source=input_lang, target=output_lang)
                                                .translate(text=text)) # Translate each sentence
            return ' '.join(translate_text) # Join the translated sentences
        except Exception as ex:
            ValueError



    async def json_decoder(self, text: str) -> dict:
        """
        This method takes a string as an argument and tries to find a JSON inside it.
        If a JSON is found, it is decoded and the value of the 'content' key is returned.
        If no JSON is found, None is returned.

        :param text: The string to be searched for a JSON
        :return: The value of the 'content' key from the JSON or None if no JSON is found
        :raises ValueError: If an error occurs during the execution of the task
        """
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                str_json = json_match.group(0)
                data = json.loads(str_json)
                return data['content']
            else:
                return None
        except Exception as ex:
            ValueError


    async def get_page(self, url: str, proxy_ip: str, login: str, password: str) -> str:
        """
        Функция для получения страницы для работи из beautifulsoup

        This method takes a URL as an argument and returns the page as a string.
        :proxy - "http://login:password@11.11.11.11:1111"
        :param url: The URL to get the page from
        :return: The page as a string
        :raises aiohttp.ClientError: If an error occurs during the execution of the task
        """
        IP_= await self.proxy_checker(proxy_ip=proxy_ip, login=login, password=password)
        full_proxy = f"http://{login}:{password}@{IP_}"
        async with aiohttp.ClientSession( 
            max_line_size=8190 * 2, 
            max_field_size=8190 * 2, 
            headers={'Accept': 'text/html'}
            ) as session:
            async with session.get(url, proxy=full_proxy) as response:
                return await response.text()
            

    def aws_ip_rotator(self, url: str, aws_access_key_id: str, aws_secret_access_key: str, **kwargs) -> str:
        """
        This method takes a URL as an argument and returns the page as a string.
        It uses the AWS gateway to get the page.

        :param url: The URL to get the page from
        :return: The page as a string
        :raises aiohttp.ClientError: If an error occurs during the execution of the task
        """
        try:
            with ApiGateway(url, access_key_id=aws_access_key_id, access_key_secret=aws_secret_access_key) as aws:
                session = requests.Session()
                session.mount(url, aws)
                return session.get(url, **kwargs)
        except Exception as ex:
            print(f"AWS gateway error: {ex}") 
            ValueError

    @staticmethod
    def pw_main(time_browser_work: int = 4, headless: bool = False, proxy: dict = None) -> Any | None:
        """ 
        При вызове функции передаете только url в виде строки
        pw_result = await some_parser('some_url')

        @mixin.pw_main(time_browser_work: int = 5, headless: bool = False, proxy: dict)
            async def some_parser(self, page, url):
                await page.goto(url)
        ::proxy - {
            "server": "http:://11.11.11.11:1111",
            "username": login,
            "password": password
            }
        ::time_browser_work - время работы браузера в секундах
        ::headless - режим браузера(если True - браузер не открывается)"""
        def decorator(function):
            """
            A decorator that sets up a Playwright browser context and page for the decorated function.

            This static method wraps a function that requires a Playwright page, handling the setup and teardown
            of the browser context. It launches a Chromium browser, creates a new context with specified settings,
            and passes a Playwright page object to the wrapped function. After the function execution, it waits
            for a short timeout before returning the result.

            :param function: The function to wrap, which should accept `self`, `page`, and `url` as arguments.
            :return: A wrapper function that sets up the Playwright environment and executes the wrapped function.
            """
            async def wrapper(self, *args): 
                playwright = await async_playwright().start()
                browser = await playwright.chromium.launch(headless=headless, proxy=proxy)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/237.84.2.178 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080})
                page = await context.new_page()
                parse_result = await function(self, page=page, url=args[0])
                await page.wait_for_timeout(time_browser_work*1000)
                await browser.close()
                await playwright.stop()
                return parse_result
            return wrapper
        return decorator
    


    async def send_data_to_srm(self, parse_data: dict, crm_url: str) -> None:
        """
        This function sends the data to the server.

        It takes a dictionary of the data which should be sent as an argument.
        The dictionary should contain the following keys:
        dict = {
            "title": title - str - the title of the news,
            "content": content - str - the content of the news,
            "image": image - str - the link to the image of the news,
            "region": "region - str - the region of the news,
            "categories_name": "categories_name - str - the name of the category of the news
        }
        If something goes wrong during the sending, it raises ValueError.
        """
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(
                        url=crm_url,
                        json=parse_data,
                        headers={"Content-Type": "application/json"}
                        )
        except Exception as ex:
            ValueError

    
    async def proxy_checker(self, proxy_ip: str, login: str, password: str) -> str:
        """Проверка прокси на работоспособность"""

        list_of_ip = [ip.strip() for ip in proxy_ip.split(',')] # разбиваем прокси на список
        
        for i in list_of_ip:
            IP_ = random.choice(list_of_ip) # выбираем рандомный прокси
            full_proxy = f"http://{login}:{password}@{IP_}" # формируем прокси
            try:
                """если в течении 3 секунд прокси работает(нет исключений), то возвращаем его,
                иначе идем дальше по списку прокси"""
                requests.get("http://google.com", proxies={'http': full_proxy, 'https': full_proxy}, timeout=3)
                return IP_
            except Exception as ex:
                print(f"IP: {IP_} error: {ex}")
                continue


    async def request_proxy(self, proxy_ip: str, login: str, password: str) -> dict:
        """рандомно генерируется прокси для запросов через aiohttp и requests"""
        IP_ = await self.proxy_checker(proxy_ip=proxy_ip, login=login, password=password)
        full_proxy = f"http://{login}:{password}@{IP_}"
        return {'http': full_proxy, 'https': full_proxy}
    
    
    async def pw_proxy(self, proxy_ip: str, login: str, password: str) -> dict:
        """рандомно генерируется прокси для запросов через krawl4ai и playwright"""
        IP_ = await self.proxy_checker(proxy_ip=proxy_ip, login=login, password=password)
        return {
            'server':  f"http://{IP_}", 
            'username': login, 
            'password': password}
