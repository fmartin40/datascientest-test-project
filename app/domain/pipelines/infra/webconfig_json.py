from app.domain.pipelines.entities.website import WebConfig
from app.domain.pipelines.interfaces.iweb_config import IWebconfig

class WebConfigJson(IWebconfig):
    def get_website_config(website: str) -> WebConfig:
        match website:
            case "emplois-informatique":
                return WebConfig(
                    name="emplois-informatique",
                    url_summaries="",
                    url_detail="https://www.emplois-informatique.fr/cdi/data-engineer-dsi-groupe-6837948",
                    tag={"type": "application/ld+json"},
                )
            case "glassdoor":
                return WebConfig(
                    name="glassdoor",
                    url_summaries="",
                    url_detail="https://www.glassdoor.fr/Emploi/paris-75-france-data-engineer-emplois-SRCH_IL.0,15_IC2881970_KO16,29.htm",
                    tag={"id": "__NEXT_DATA__"},
                )
            case "jobintree":
                return WebConfig(
                    name="jobintree",
                    url_summaries="https://www.jobintree.com/emploi/recherche.html?k={job}&l={place}",
                    url_detail="https://www.jobintree.com/emplois/60831578.html",
                    tag={"type": "application/ld+json"},
                    detail_pattern={
                        "title": "title",
                        "company": "hiringOrganization.name",
                        "city": "jobLocation.address.addressLocality",
                        "postal_code": "jobLocation.address.postalCode",
                        "type": "employmentType",
                        "description": "description",
                        "required": ["title", "description"]
                    },
                )
            case "muse":
                return WebConfig(
                    name="muse",
                    url_summaries="",
                    url_detail="https://www.themuse.com/jobs/atlassian/senior-manager-data-science-6df833",
                    tag={"id": "__NEXT_DATA__"},
                    detail_pattern={
                        "title": "props.pageProps.initialAppParams.job.name",
                        "company": "props.pageProps.initialAppParams.company.name",
                        "city": ("props.pageProps.initialAppParams.job.locations", ["city"]),
                        "postal_code": "",
                        "type": "props.pageProps.initialAppParams.job.employmentTypes",
                        "description": "props.pageProps.initialAppParams.job.compiled_contents",
                        "required": ["props", "query"]
                    },
                )
            case "optioncarriere":
                return WebConfig(
                    name="option_carriere",
                    url_summaries="",
                    url_detail="https://www.optioncarriere.com/jobad/fraf74734f528917804df9de514029dbb4",
                    tag={"type": "application/ld+json"},
                )
            case _:
                raise ValueError(f"Configuration inconnue pour le site : {website}")
