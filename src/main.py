"""
TimesJobs.com Scraper - Main Module
Extracts job listings from TimesJobs.com for AI agents and MCP integrations
"""

import asyncio
import re
from typing import Dict, List, Optional
from urllib.parse import quote_plus, urljoin

import httpx
from apify import Actor
from bs4 import BeautifulSoup


class TimesJobsScraper:
    """Scraper for TimesJobs.com job listings"""
    
    BASE_URL = "https://www.timesjobs.com"
    SEARCH_URL = "https://www.timesjobs.com/candidate/job-search.html"
    
    def __init__(self, proxy_config: Optional[Dict] = None):
        """Initialize the scraper with optional proxy configuration"""
        self.proxy_config = proxy_config
        self.jobs_scraped = 0
        
    async def build_search_url(self, keywords: str, location: str, page: int = 1) -> str:
        """Build the search URL with parameters"""
        params = {
            'searchType': 'personalizedSearch',
            'from': 'submit',
            'txtKeywords': keywords,
            'txtLocation': location,
        }
        
        if page > 1:
            params['sequence'] = str(page)
            
        query_string = '&'.join([f"{k}={quote_plus(str(v))}" for k, v in params.items()])
        return f"{self.SEARCH_URL}?{query_string}"
    
    async def fetch_page(self, url: str, client: httpx.AsyncClient) -> Optional[str]:
        """Fetch a page with proxy support"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = await client.get(url, headers=headers, follow_redirects=True, timeout=30.0)
            response.raise_for_status()
            return response.text
            
        except Exception as e:
            Actor.log.exception(f"Error fetching {url}: {e}")
            return None
    
    async def parse_job_card(self, card: BeautifulSoup) -> Optional[Dict]:
        """Parse a single job card element"""
        try:
            job = {}
            
            # Job title
            title_elem = card.select_one('h2 a, h3 a, .jobTitle, .title')
            if title_elem:
                job['jobTitle'] = title_elem.get_text(strip=True)
                job['jobLink'] = urljoin(self.BASE_URL, title_elem.get('href', ''))
            else:
                return None
            
            # Company name
            company_elem = card.select_one('.joblist-comp-name, .companyName, h3.joblist-comp-name')
            if company_elem:
                job['companyName'] = company_elem.get_text(strip=True)
            
            # Location
            location_elem = card.select_one('.location, .loc, [class*="location"]')
            if location_elem:
                job['location'] = location_elem.get_text(strip=True)
            
            # Experience
            exp_elem = card.select_one('.experience, .exp, [class*="experience"]')
            if exp_elem:
                job['experience'] = exp_elem.get_text(strip=True)
            
            # Salary
            salary_elem = card.select_one('.salary, .sal, [class*="salary"]')
            if salary_elem:
                job['salary'] = salary_elem.get_text(strip=True)
            else:
                job['salary'] = 'Not Disclosed'
            
            # Skills
            skills_container = card.select_one('.srp-skills, .skills, [class*="skill"]')
            if skills_container:
                skills = skills_container.get_text(strip=True)
                job['skills'] = re.sub(r'\s+', ' ', skills)
            
            # Job description
            desc_elem = card.select_one('.list-job-dtl, .job-description, [class*="description"]')
            if desc_elem:
                job['jobDescription'] = desc_elem.get_text(strip=True)[:500]
            
            # Posted date
            date_elem = card.select_one('.sim-posted, .postDate, [class*="posted"]')
            if date_elem:
                job['postedDate'] = date_elem.get_text(strip=True)
            
            # Clean up the data
            for key in job:
                if isinstance(job[key], str):
                    job[key] = re.sub(r'\s+', ' ', job[key]).strip()
            
            return job if job.get('jobTitle') else None
            
        except Exception as e:
            Actor.log.warning(f"Error parsing job card: {e}")
            return None
    
    async def scrape_search_page(self, html: str) -> List[Dict]:
        """Extract jobs from a search results page"""
        jobs = []
        
        try:
            soup = BeautifulSoup(html, 'lxml')
            
            # Try multiple selectors for job cards
            job_cards = (
                soup.select('.clearfix.job-bx') or
                soup.select('li.clearfix') or
                soup.select('.job-bx') or
                soup.select('[class*="job-"]') or
                soup.select('li')
            )
            
            Actor.log.info(f"Found {len(job_cards)} potential job cards")
            
            for card in job_cards:
                job = await self.parse_job_card(card)
                if job:
                    jobs.append(job)
                    self.jobs_scraped += 1
                    
        except Exception as e:
            Actor.log.exception(f"Error parsing search page: {e}")
        
        return jobs
    
    async def scrape_jobs(
        self,
        keywords: str,
        location: str = "",
        max_results: int = 50,
        experience_level: str = ""
    ) -> List[Dict]:
        """Main scraping function"""
        all_jobs = []
        page = 1
        max_pages = (max_results // 20) + 1  # TimesJobs typically shows ~20 jobs per page
        
        Actor.log.info(f"Starting scrape: keywords='{keywords}', location='{location}', max_results={max_results}")
        
        # Set up HTTP client with proxy if configured
        proxy_url = None
        if self.proxy_config:
            if self.proxy_config.get('useApifyProxy'):
                groups = self.proxy_config.get('apifyProxyGroups', ['RESIDENTIAL'])
                proxy_url = Actor.create_proxy_url(groups)
                Actor.log.info(f"Using Apify Proxy with groups: {groups}")
        
        async with httpx.AsyncClient(proxy=proxy_url, timeout=30.0) as client:
            while len(all_jobs) < max_results and page <= max_pages:
                search_url = await self.build_search_url(keywords, location, page)
                Actor.log.info(f"Fetching page {page}: {search_url}")
                
                html = await self.fetch_page(search_url, client)
                
                if not html:
                    Actor.log.warning(f"Failed to fetch page {page}, stopping")
                    break
                
                jobs = await self.scrape_search_page(html)
                
                if not jobs:
                    Actor.log.info(f"No jobs found on page {page}, stopping")
                    break
                
                all_jobs.extend(jobs)
                Actor.log.info(f"Scraped {len(jobs)} jobs from page {page} (total: {len(all_jobs)})")
                
                if len(jobs) < 10:  # If we get very few results, probably no more pages
                    break
                
                page += 1
                await asyncio.sleep(1)  # Be polite
        
        # Limit to max_results
        return all_jobs[:max_results]


async def main():
    """Main entry point for the Apify Actor"""
    async with Actor:
        Actor.log.info("TimesJobs Scraper starting...")
        
        # Get input
        actor_input = await Actor.get_input() or {}
        
        search_keywords = actor_input.get('searchKeywords', 'Python Developer')
        search_location = actor_input.get('searchLocation', '')
        max_results = actor_input.get('maxResults', 50)
        experience_level = actor_input.get('experienceLevel', '')
        proxy_config = actor_input.get('proxyConfig')
        
        Actor.log.info(f"Input: keywords={search_keywords}, location={search_location}, max={max_results}")
        
        # Initialize scraper
        scraper = TimesJobsScraper(proxy_config=proxy_config)
        
        # Scrape jobs
        jobs = await scraper.scrape_jobs(
            keywords=search_keywords,
            location=search_location,
            max_results=max_results,
            experience_level=experience_level
        )
        
        Actor.log.info(f"Scraped {len(jobs)} total jobs")
        
        # Push to dataset
        if jobs:
            await Actor.push_data(jobs)
            Actor.log.info(f"✅ Successfully pushed {len(jobs)} jobs to dataset")
        else:
            Actor.log.warning("⚠️ No jobs found - check your search parameters or site structure may have changed")
        
        Actor.log.info("Scraper finished")


if __name__ == "__main__":
    asyncio.run(main())
