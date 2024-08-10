import requests
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5,ko;q=0.4,fr;q=0.3",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "s-ha-lvt-d5f6f70b27f841099b2c694431c78e4e=1715575903226; s-ha-lvt-d5f6f70b27f841099b2c694431c78e4e=1715575900675; acw_tc=b65cfd2817155758923117148e24a266bf4770c949ab940f9672fe53eafd02; C_UNDEFINED=Yjg5Mzg0YzUtN2ZjNi00OGQzLTlkNGQtZGI3OWE4YzA5Y2Nj; Hm_lvt_f90049d755593aa0e687490df92d9ca4=1715416088,1715575895; s-ha-lvt-d5f6f70b27f841099b2c694431c78e4e=1715575895112; Hm_lpvt_f90049d755593aa0e687490df92d9ca4=1715575958; UM_UNDEFINED=QlMbsJgtGTCvtZo7O36DUsiIsqY68rS032sSyPTSsQkVV4yMoQ6y0A==; tfstk=f_Zibs_yrPu1tLpAskm1Y-o_aM_LCCib0SKxMmhV8XlQXxB1GiDqtSqtDNw4iqPr9l3xb1g2m7NMDfPA5IS4w-hwb1G2mekoEtGV5x-miANRCl3q32-0MSNmlOGxgjVY3PBd2ge_CmiVm_IR2YmIw7EigIn2XD37R_CR2Me_CmiVwrQwZEenhXkZQh8NKMktTxk4gfueTYDS0jPq09mEexhq3Vlq82lyAnlu0kZFe5VBuKEz0kDi8weiTnDLxA0ZaRrM0n8rIVczQX1RSScm8-g0cKtmTRz7GYPw__3_3yVnImjp70y3u7DQbgdidPeUeXykU3ytjlem_57ABJqms4rZ-KKuEcH4gq4CZ3HiXy0ujP6XTRP-szo_HLfTK44nPvuenFoTy8EjzlSMNX3Sn5hLag-nYqSrxe8y7ctjLtEelEgZdvc51E4kKLpUoNBhKU_s7vMOw9XHlEgZdvcRK9YWGVkIB_C..; ssxmod_itna=YqRx9Wi=DQ0=oD5GHD8D2Y6=k3ZYdDujinmO1px05veGzDAxn40iDtooTx6Y=jQGxmKf7e3qhsjF0wPmGft7ic4fOmDB3DEx06iql=xii9DCeDIDWeDiDG+=DFxYoDeoHQDFF5X/ZcpxAQDQ4GyDitDKq0cDi3DA4DjFw45F7=DI4GfDDfn7n6PDDXPYPAKGYeDbO=SnRiDreDS4htdj7=DjqGgDBLeBcbDGLysHiNSAc9WaEQ4oeGuDG6Ppwdex0PyBut2bc53WOD3mAvxIYxF424YYGRiQ7lyOAx2o7eo4Eh=KAx37B3dnqQjG=PiQ7dsQDxD=; ssxmod_itna2=YqRx9Wi=DQ0=oD5GHD8D2Y6=k3ZYdDujinmO1xnF8qPDsi1DL7Pb7ove9UB4n43O/AYL2NdqeKfB2P4T8e7bsdwRrYrLeERe7+vRQClM0Uxg81EXXFkYmZ260x3XMDv/Q79ZSZ7=T9CHaIaSh9rBBqWwZ5xViGiBePsop0NlogpGoFsDcPeGPp8ORpvFPSrRBmrBpOLn7hdXR8mRe+doIOUQhufBFLrMKQ0VSm74HjQimlRZIwdogknQ=6rdo6fQ6n+opOcVfk9qMdPS=iydQ0RTd9c8dUdertlRunFOtSMIKNfmapd/womOrmodlwiUi=VwQSOCR7D5mYXAtKhh9M=4WY=eG8Ws0OdkW=sjwFqwKOdKC3ElNpehoSso+k3hHcbQBxIekFR3vDdPD7je7xYDrdGqdY4yGmiA5YCLwbwMjepf5mixdaWA34AUWpcwvFqqBemAqAIGwOnp39xiFYBa2UnmtD3n6KBWn8GBtHOiDv/FqD3p4EMejM4Bx7w+BAvfqwFDwbxiGdC07AzqpOxDjKDeuLFYjhAO4PHLZxeZtbzq=qnbKXf/jG1n=k6r7n1tepL9b/C=dne7AbUuKGxgzxoDe4D=",
    "Host": "credit.acla.org.cn",
    "Referer": "https://credit.acla.org.cn/credit/lawFirm/1ae69d168007be77220774583db56ecbf9c9733440ab7e10ecdceabe4998e91d9b10170679444c7a9f6b32f6201e492f",
    "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
}
url = "https://credit.acla.org.cn/credit/lawFirm/1ae69d168007be77220774583db56ecbf9c9733440ab7e10ecdceabe4998e91d9b10170679444c7a9f6b32f6201e492f?refer__1711=YqAxgDuD9DBAi%3DD%2FD0ex2DU2%2FzBvO8077bD&alichlgref=https%3A%2F%2Fcredit.acla.org.cn%2Fcredit%2FlawFirm%3FpicCaptchaVerification%3D%26keyWords%3D%25E5%258C%2597%25E4%25BA%25AC%25E5%2592%258C%25E5%2584%2592%26refer__1711%3Dn4mx0DyDgD9DuDfxiwRxBu7x2GniY4eDt31%252BQ4D%26alichlgref%3Dhttps%253A%252F%252Fcredit.acla.org.cn%252F#allow"
response = requests.get(url, headers=headers)
print(response.text)