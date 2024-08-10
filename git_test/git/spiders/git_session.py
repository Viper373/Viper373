import scrapy


class GitSessionSpider(scrapy.Spider):
    name = "git_session"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/login"]

    def parse(self, response):
        # 从登录页面响应中解析出post数据
        token = response.xpath('//input[@name="authenticity_token"]/@value').extract_first()
        timestamp = response.xpath('//input[@name="timestamp"]/@value').extract_first()
        timestamp_secret = response.xpath('//input[@name="timestamp_secret"]/@value').extract_first()
        post_data = {
            "commit": "Sign in",
            "authenticity_token": token,
            "login": "viper373",
            "password": "ShadowZed666",
            "webauthn-conditional": "undefined",
            "javascript-support": "true",
            "webauthn-support": "supported",
            "webauthn-iuvpaa-support": "supported",
            "return_to": "https://github.com/login",
            "allow_signup": "",
            "client_id": "",
            "integration": "",
            "required_field_29b0": "",
            "timestamp": timestamp,
            "timestamp_secret": timestamp_secret
        }
        # print(post_data)
        # 针对登录url发送post请求
        yield scrapy.FormRequest(
            url="https://github.com/session",
            callback=self.after_login,
            formdata=post_data
        )

    def after_login(self, response):
        yield scrapy.Request('https://github.com/Viper373', callback=self.check_login)

    def check_login(self, response):
        print(response.xpath('/html/head/title/text()').extract_first())
