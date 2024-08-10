import scrapy


class GitFirstSpider(scrapy.Spider):
    name = "git_first"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/Viper373"]

    def start_requests(self):
        url = self.start_urls[0]
        temp = '_octo=GH1.1.1122720337.1707412288; _device_id=a78d8cbfc6b6929677d5c2d8e1fa9e91; saved_user_sessions=77206948%3A5otGR0uA1Jztgv2dxxdUHz8GeL5-HJ8t8_ZXsLkOdU5Q-1Pw; user_session=5otGR0uA1Jztgv2dxxdUHz8GeL5-HJ8t8_ZXsLkOdU5Q-1Pw; __Host-user_session_same_site=5otGR0uA1Jztgv2dxxdUHz8GeL5-HJ8t8_ZXsLkOdU5Q-1Pw; logged_in=yes; dotcom_user=Viper373; has_recent_activity=1; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; preferred_color_mode=light; tz=Asia%2FShanghai; _gh_sess=1jhxueU9NJLx08hxTZFuOi6iGafZ0NBqOv42vyCxfq1ru8fh0yPX7Vk8FVp4CtCAmQfmVrPjqnKqNAaWf%2FjVFJ3mnoH5EKmZScAuuc0m9UPFw78f7j2zJhBRqMDJi0EE6VrikU4H9FtkpNilqvgKjkjf2Jpz%2BRDCyYWQfIdtFgy2eEjaBkvJGI%2BauAn3cZhT3i169CWHJa11i1L6qolUkq%2BRlpMMZsxDJoKWHSsB99RhyUV5q6GwqmPN89wyUJtY2Rew7GCnHklKsXb1Ti30O5sL5D16p6DU24IWWb678dBTrmTOQbF9nljTZi4npJSYGrLdigGpTDLmFKs%2F14Hn77l6vbfGhcBq2l07WLggBRmaEa0Gn%2Bt1npHUK%2FB6eHvIeWRvQMNU%2FSXBI7GeQ26%2FyftvnSssLpYPR6hZeOXiLLoKB%2B%2BdKioY3eIWnJd8TYq87kRHkHfnRzmPCCh0xpKfWxNhrS2t8jqRhfpShydZNP%2BOLRwHq9FYroJC2ut9IJH4P8f3MBdviet8t62k3oHFtA2KU1nNWfwg--ft3ef7cz5uC6uKxb--i0VjDENAHQgrvitnsg5QkA%3D%3D'
        cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split('; ')}
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            cookies=cookies,
        )
    def parse(self, response):
        print(response.xpath('/html/head/title/text()').extract_first())