from app.domain.pipelines.entities.extractconfig import ExtractConfig
from app.domain.pipelines.interfaces.iconfig_service import IConfigService

class WebConfigJson(IConfigService):
    def get_website_config(self, website: str) -> ExtractConfig:
        match website:
            case "emplois-informatique":
                return ExtractConfig(
                    name="emplois-informatique",
                    url_summaries="",
                    url_detail="https://www.emplois-informatique.fr/cdi/data-engineer-dsi-groupe-6837948",
                    tag={"type": "application/ld+json"},
                )
            case "glassdoor":
                return ExtractConfig(
                    name="glassdoor",
                    url_summaries="",
                    url_detail="https://www.glassdoor.fr/Emploi/paris-75-france-data-engineer-emplois-SRCH_IL.0,15_IC2881970_KO16,29.htm",
                    tag={"id": "__NEXT_DATA__"},
                )
            case "jobintree":
                return ExtractConfig(
                    name="jobintree",
                    url_summaries="https://www.jobintree.com/emploi/recherche.html?k={job}&l={place}",
                    
                    tag={"type": "application/ld+json"},
                    detail_pattern={
                        "title": "title",
                        "company": "hiringOrganization.name",
                        "city": "jobLocation.address.addressLocality",
                        "postal_code": "jobLocation.address.postalCode",
                        "contract_type": "employmentType",
                        "description": "description",
                        "required": ["title", "description"]
                    },
                )
            case "muse":
                return ExtractConfig(
                    name="muse",
                    url_summaries="",
                    url_detail="https://www.themuse.com/jobs/atlassian/senior-manager-data-science-6df833",
                    tag={"id": "__NEXT_DATA__"},
                    detail_pattern={
                        "title": "props.pageProps.initialAppParams.job.name",
                        "company": "props.pageProps.initialAppParams.company.name",
                        "city": ("props.pageProps.initialAppParams.job.locations", ["city"]),
                        "postal_code": "",
                        "contract_type": "props.pageProps.initialAppParams.job.employmentTypes",
                        "description": "props.pageProps.initialAppParams.job.compiled_contents",
                        "required": ["props", "query"]
                    },
                )
            case "optioncarriere":
                return ExtractConfig(
                    name="option_carriere",
                    url_summaries="",
                    url_detail="https://www.optioncarriere.com/jobad/fraf74734f528917804df9de514029dbb4",
                    tag={"type": "application/ld+json"},
                )
            case _:
                raise ValueError(f"Configuration inconnue pour le site : {website}")

    def create_website_config(self, extract_service: ExtractConfig) -> ExtractConfig:
        raise NotImplementedError