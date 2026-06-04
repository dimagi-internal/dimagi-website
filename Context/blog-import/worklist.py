# Categorize the dimagi.com post-sitemap into editorial vs excluded, minus already-built.
import os, re

ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login"
built = set(d for d in os.listdir(os.path.join(ROOT,"blog")) if os.path.isdir(os.path.join(ROOT,"blog",d)))

# Full post-sitemap (slug, lastmod) pulled 2026-06-03
RAW = """
bao-systems-and-dimagi-announce-integration-partnership 2023-12-15
http-www-oikoi-io 2023-12-15
im-saf 2023-12-15
illimitis 2023-12-15
statinfo 2023-12-15
it4life 2023-12-15
bongohive 2023-12-15
goodcitizen 2023-12-15
compelling-works 2023-12-15
instrat 2023-12-15
digital-health 2023-12-15
brotecs 2023-12-15
enigma 2023-12-15
gicmed 2023-12-15
innovastra 2023-12-15
webalive 2023-12-15
bao 2023-12-15
openfn 2023-12-15
a-day-in-the-life-of-dhivya-sivaramakrishnan 2023-12-15
commcare-provider-program 2023-12-15
addressing-vermonts-housing-crisis-through-a-targeted-tech-driven-approach 2023-12-15
a-day-in-the-life-of-themba-nyirenda-senior-technical-project-analyst-solutions-division 2023-12-15
malawi-ministry-of-health-cstock-supply-chain-management-application 2023-12-15
digital-development-organizations-take-away-it-security-news 2023-12-15
dimagi-acquires-sureadhere-digital-solutions 2023-12-15
adpp-mozambique-tb-local-response 2023-12-15
dimagis-5-year-strategy 2023-12-15
three-digital-tools-for-behavioral-health 2023-12-15
thriving-in-a-hybrid-world 2023-12-15
digital-solutions-scale-mental-health-care 2023-12-15
reducing-childhood-malnutrition-in-madagascar 2023-12-15
high-impact-growth-podcast 2023-12-15
4-reasons-to-jump-into-a-social-impact-career-now 2023-12-15
dimagi-monkeypox-case-management-solution 2023-12-15
digital-health-must-invest-in-local-digital-ecosystems 2023-12-15
commcare-grant-2022-winners 2023-12-15
global-digital-health-forum-2022 2023-12-15
celebrating-20-years-of-impact 2023-12-15
tech-team-summit-2022 2023-12-15
vermont-care-network 2023-12-15
researcher-spotlight-nick-tarantino 2023-12-15
researcher-spotlight-jack-hetherington 2023-12-15
commcare-in-the-classroom 2023-12-15
commcare-grant-awardee-series-introduction 2023-12-15
international-workers-day-2023 2023-12-15
introducing-wellme-the-resilience-app-for-frontline-workers 2023-12-15
a-day-in-the-life-of-wouter-vink 2023-12-15
covid-19-pandemic-preparedness-report 2023-12-15
two-big-lessons-that-iowa-and-geneva-can-teach-us-about-technology-in-digital-development 2023-12-15
join-the-fight-to-support-critical-open-source-infrastructure 2023-12-15
theres-no-choice-but-to-act-now-who-contact-tracing-template-app-available-today 2023-12-15
great-reset-social-enterprise-wef 2023-12-15
covid-19-equitable-vaccine-delivery 2023-12-15
reflecting-on-2020 2023-12-15
innovation-at-dimagi-part-2-approach-to-failure 2023-12-15
innovation-at-dimagi-part-4-innovation-funding 2023-12-15
abt-associates-vaccine-hesitancy-cbos 2023-12-15
innovation-at-dimagi-part-6-new-business-portfolio 2023-12-15
zohaib-ali-khusru 2023-12-15
namaste 2023-12-15
wellme-update2 2023-12-15
a-day-in-the-life-of-charles-aphrem 2023-12-15
my-time-at-dimagi-as-an-intern 2023-12-15
a-day-in-the-life-of-aubrey-chirwa-senior-technical-project-analyst-solutions-division 2023-12-15
grand-challenges-catalyzing-equitable-ai 2023-12-15
dimagi-to-host-its-inaugural-commcare-enterprise-summit-to-drive-impact-delivery 2023-12-15
commcare-research-grant-checkin-move-up-global 2024-05-14
ecd-digital-transformation 2024-05-14
ict4d-conf-2024 2024-05-14
world-poultry-foundation-guide 2024-05-14
design-thinking 2024-05-14
commcare-connect-2023 2024-05-14
island-health-care 2024-05-14
career-journey-of-simon-kelly 2024-05-14
enterprise-summit-2023 2024-05-14
career-journey-of-julia-fuller 2024-05-28
commcare-connect-reaches-100000-deliveries 2024-05-31
expedite-your-case-management-workflows-introducing-case-list-explorer 2024-06-05
johnson-johnson-foundation-leveraging-advanced-analytics-to-develop-engagement-profiles 2024-06-05
20-years-of-designing-under-the-mango-tree 2024-06-05
what-we-learned-from-our-working-group-on-health-worker-wellbeing 2024-06-05
dimagi-receives-25-million-to-develop-transformative-technology-for-frontline-workers 2024-06-05
gorongosa-national-park-mozambique-nutrition-behavioral-change-sms 2024-06-05
work-life-balance-in-2022 2024-06-05
abt-associates-healthy-mother-healthy-baby-tajikistan 2024-06-05
learnings-from-5-years-of-new-business 2024-06-05
pathfinder-youth-voices-for-agency-and-access-yuvaa-india 2024-06-05
global-fund-partnership 2024-06-05
global-digital-health-forum-2021 2024-06-05
johnson-and-johnson-foundation-commcare-companion-application 2024-06-05
national-institutes-of-health-survivorcare-phase-ii 2024-06-05
find-covid-19-rdt-solution 2024-06-05
building-in-the-open-september-2021 2024-06-05
vaccine-solution-covid-19-routine-immunization 2024-06-05
innovation-at-dimagi-part-7-van-westendorp-price-sensitivity-model 2024-06-05
terre-des-hommes-covid-19-jharkhand 2024-06-05
catholic-relief-services-technical-advisory-services-2021 2024-06-05
tdh-covid-19-case-screening 2024-06-05
dimagi-climate-pledge-2021 2024-06-05
commcare-precision-tasking-framework 2024-06-05
baobab-senegal-uncdf-commbanane-advisory-service 2024-06-05
undp-financial-education-application 2024-06-05
crisis-response-corps-launch 2024-06-05
commcare-fhir-integration 2024-06-05
inc-5000-list-2021 2024-06-05
jamaica-commcare-covid19-vaccination-platform 2024-06-05
user-testing-chw-resilience-messaging 2024-06-05
climate-neutral-certified 2024-06-05
building-in-the-open-june-2021 2024-06-05
journey-to-self-reliance-usaid-onse-malawi 2024-06-05
find-antigen-rdt-pm-training 2024-06-05
innovation-at-dimagi-part-5-innovation-lifecycle 2024-06-05
covid-19-pro-bono-project-highlights-2021 2024-06-05
fast-company-world-changing-ideas-2021 2024-06-05
tufts-iita-inddex24-nigeria 2024-06-05
somalia-who-covid-19-vaccination-management-platform 2024-06-05
egpaf-malawi-pepfar-gh002301 2024-06-05
building-in-the-open-march-2021 2024-06-05
teuk-saat-1001-local-ownership 2024-06-05
cdc-foundation-pods-project 2024-06-05
rti-international-usaid-iecd-activity 2024-06-05
innovation-at-dimagi-part-3-evaluating-the-mission 2024-06-05
data-driven-program-improvements-webinar-miraclefeet 2024-06-05
building-in-the-open-february-2021 2024-06-05
covid-19-equitable-vaccine-delivery-challenges 2024-06-05
covid-19-distribution-equitable-des-vaccins 2024-06-05
banyan-global-empleando-futuros 2024-06-05
innovation-at-dimagi-part-1-dedicated-entrepreneur 2024-06-05
global-digital-health-forum-2020 2024-06-05
mobile-data-collection-commcare-tuberculosis 2024-06-05
ndoh-national-scale-mhealth-south-africa 2024-06-05
usaid-advancing-nutrition-2020 2024-06-05
miraclefeet-covid-19-qa 2024-06-05
google-org-medic-mobile-covid-19-flw-support 2024-06-05
usaid-global-health-innovation-index-commcare-2020 2024-06-05
solutions-remote-impact-covid-19 2024-06-05
covid-19-africa-commcare 2024-06-05
covid-19-recherche-des-contacts-jhu-commcare 2024-06-05
covid-19-aws-contact-tracing 2024-06-05
covid-19-recherche-des-contacts-anne-liu 2024-06-05
contact-tracing-2014-ebola-anne-liu 2024-06-05
covid-19-response-jhu-digital-solutions-report 2024-06-05
riposte-covid-19-modeles-dapplications 2024-06-05
riposte-covid-19-modeles-doutils-bi 2024-06-05
covid-19-template-application-port-of-entry 2024-06-05
covid-19-template-application-healthcare-provider-training-monitoring 2024-06-05
opioid-epidemic-nascare-course 2024-06-05
covid-19-template-application-facility-readiness 2024-06-05
covid-19-template-bi-tools 2024-06-05
sentinel-audacious-project-2020 2024-06-05
covid-19-response-template-apps 2024-06-05
sf-ucsf-contact-tracing-announcement 2024-06-05
sierra-leone-directorate-of-science-technology-and-innovation-covid-19-response 2024-06-05
who-covid-19-contact-tracing-template-application-released 2024-06-05
mobile-data-collection-cash-transfer-programs 2024-06-05
coronavirus-covid-19-response-initiative 2024-06-05
field-research-storytelling 2024-06-05
dimagi-awards 2024-06-05
field-research-card-sorting 2024-06-05
baylor-college-of-medicine-ethics-lesotho 2024-06-05
mhealth-interventions-bmc-macdonald 2024-06-05
healthcare-in-pima-county-arizona 2024-07-03
dimagi-renews-its-commitment-to-the-global-fund-with-a-5-million-pledge 2024-08-23
miraclefeet-drives-global-impact-through-commcare-and-the-impact-delivery-approach 2024-09-25
wielding-the-power-of-data-for-violence-reduction-and-prevention 2024-10-21
givewell-awards-dimagi-funding-to-enhance-child-health-service-delivery-in-nigeria 2024-11-13
commcare-provider-profile-how-oikoi-is-digitizing-data-collection-for-agriculture 2024-11-13
gtd-summit-2024-recap 2024-11-15
strengthening-mental-health-services-with-digital-solutions 2024-11-15
usaid-div-and-dimagi-partner-to-enhance-child-health 2024-11-22
gdhf-2024 2024-11-27
harnessing-ais-potential-to-improve-equity 2025-03-04
building-a-culture-of-continuous-learning-at-dimagi 2025-03-04
behind-our-b 2025-03-04
sureadheres-story 2025-03-18
refreshing-dimagi-and-commcare-brands-for-high-impact-growth 2025-06-03
mercy-corps-guide-to-building-a-digital-ecosystem-for-me-at-scale 2025-06-03
your-ultimate-accessibility-guide-designing-for-inclusion-and-empowering-all-users 2025-06-03
five-talents-savings-groups 2025-07-17
digital-tools-public-health-workers 2025-07-21
unicef-health-campaign-digitalization-guidebook 2025-08-28
commcare-eu-cloud-launch 2025-09-10
case-management-course-dimagi-academy 2025-10-08
inaugural-commcare-government-summit 2025-10-10
whats-new-in-commcare-fall-2025 2025-10-20
build-mobile-data-collection-app 2025-11-11
how-to-choose-data-collection-tool 2025-11-11
no-code-app-builder-program-teams 2025-11-11
closing-post-discharge-gap-kangaroo-mother-care 2025-11-17
tech-enabled-approach-to-community-health-care 2025-11-17
harnessing-ai-for-frontline-workers 2025-11-17
frontline-worker-advisory-panel-launch 2025-11-17
2024-year-in-review 2025-11-18
supporting-our-partners 2025-11-18
dimagi-makes-the-inc-5000-list-for-the-tenth-time 2025-11-19
global-digital-health-forum-2025 2025-11-21
how-to-collect-data-offline 2025-12-12
commcare-use-cases-operational-efficiency 2025-12-16
predictive-analytics-public-health-malnutrition 2025-12-18
how-to-choose-case-management-software-frontline-teams 2026-02-13
chatbots-support-the-right-to-health 2026-02-13
day-in-the-life-of-namrata-tomar-project-manager-solutions-division 2026-02-13
riya-singh 2026-02-13
grassroot-soccer-adols 2026-02-13
tackle-africa-commcare-grant 2026-02-13
service-delivery-case-management 2026-02-28
case-study-guinea-digitized-national-malaria-campaign 2026-02-19
different-kind-of-tech-company 2026-02-25
5-ways-automate-frontline-workflows-case-management 2026-02-27
scaling-global-health-programs-a-miraclefeet-case-study 2026-04-16
taroworks-alternative-givedirectly-cash-transfer-case-study 2026-04-17
irc-data-fragmentation-standardization-case-study 2026-05-08
jsi-government-of-ethiopia-and-usaid-digital-health-activity 2026-05-14
"""

rows = [ln.split() for ln in RAW.strip().splitlines()]
rows = [(r[0], r[1]) for r in rows]

# Provider directory profiles (the 2023-12-15 short company-name cluster)
PROVIDERS = {"http-www-oikoi-io","im-saf","illimitis","statinfo","it4life","bongohive",
 "goodcitizen","compelling-works","instrat","digital-health","brotecs","enigma","gicmed",
 "innovastra","webalive","bao","openfn","namaste","commcare-provider-program",
 "commcare-provider-profile-how-oikoi-is-digitizing-data-collection-for-agriculture"}

# French-language duplicate pages
FRENCH = {"covid-19-distribution-equitable-des-vaccins","covid-19-recherche-des-contacts-jhu-commcare",
 "covid-19-recherche-des-contacts-anne-liu","riposte-covid-19-modeles-dapplications",
 "riposte-covid-19-modeles-doutils-bi"}

# SEO / product landing pages (not editorial)
SEO = {"build-mobile-data-collection-app","how-to-choose-data-collection-tool",
 "no-code-app-builder-program-teams","how-to-collect-data-offline",
 "how-to-choose-case-management-software-frontline-teams","service-delivery-case-management",
 "5-ways-automate-frontline-workflows-case-management"}

def is_person(slug):
    return (slug.startswith("a-day-in-the-life-of") or slug.startswith("day-in-the-life-of")
            or slug.startswith("career-journey-of") or slug.startswith("researcher-spotlight")
            or slug in {"zohaib-ali-khusru","riya-singh","my-time-at-dimagi-as-an-intern"})

cat = {}
for slug, date in rows:
    if slug in built:
        cat[slug] = ("BUILT", date)
    elif slug in PROVIDERS:
        cat[slug] = ("provider profile", date)
    elif slug in FRENCH:
        cat[slug] = ("French duplicate", date)
    elif slug in SEO:
        cat[slug] = ("SEO/landing page", date)
    elif is_person(slug):
        cat[slug] = ("staff bio/spotlight", date)
    else:
        cat[slug] = ("EDITORIAL", date)

from collections import defaultdict
groups = defaultdict(list)
for slug,(c,date) in cat.items():
    groups[c].append((date,slug))

print("TOTAL sitemap posts:", len(rows))
for c in ["BUILT","EDITORIAL","provider profile","staff bio/spotlight","French duplicate","SEO/landing page"]:
    print(f"  {c}: {len(groups[c])}")

print("\n===== EXCLUDED (non-editorial) =====")
for c in ["provider profile","staff bio/spotlight","French duplicate","SEO/landing page"]:
    print(f"\n-- {c} ({len(groups[c])}) --")
    for date,slug in sorted(groups[c]):
        print(f"   {date}  {slug}")

ed = sorted(groups["EDITORIAL"])
print(f"\n===== EDITORIAL TO IMPORT ({len(ed)}) =====")
for date,slug in ed:
    print(f"   {date}  {slug}")

# write editorial worklist for the workflow
with open("/tmp/editorial_worklist.txt","w") as f:
    for date,slug in ed:
        f.write(f"{slug}\t{date}\n")
print(f"\nwrote /tmp/editorial_worklist.txt ({len(ed)} slugs)")
