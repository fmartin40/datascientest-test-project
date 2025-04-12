from typing import Dict

from app.workers.common.entities.jobs import JobDetail
from app.workers.common.entities.settings import ParserSettings, WebsiteInfo
from app.workers.common.interfaces.itransformer import ITransformer


# class JobDetailFromHTMLTransformer(ITransformer):
# 	def __init__(self, website_info: WebsiteInfo, parser: ParserSettings):
# 		self.website_info: WebsiteInfo = website_info
# 		self.parser: ParserSettings = parser

# 	async def transform(self, content: str) -> dict:
# 		soup = BeautifulSoup(content, 'html.parser')
# 		extracted_data = {}
# 		for key, selector in self.parser.selectors.items():
# 			element = soup.select_one(selector)
# 			extracted_data[key] = element.get_text(strip=True) if element else None
# 		return extracted_data


class LLMTransformer(ITransformer):
	def __init__(self, website_info: WebsiteInfo, parser: ParserSettings):
		self.website_info: WebsiteInfo = website_info
		self.parser: ParserSettings = parser
		self.jobdetail: JobDetail = None

	async def transform(self, jobdetail: JobDetail) -> Dict:
		self.jobdetail = jobdetail
		raise NotImplementedError
	