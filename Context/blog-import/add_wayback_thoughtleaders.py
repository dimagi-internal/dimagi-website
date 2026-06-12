# One-off: restore 7 deleted Dimagi blog posts recovered from the WordPress export
# (they survive in the Wayback Machine but were dropped from the live/staging site).
# Bodies are faithfully reformatted into the house article style; covers/inline
# images are pulled from the live dimagi.com CDN where they survive, else an
# on-brand local asset (noted per post).
#
# Wires each post into: rendered page, listing grid, sitemap, tag_overrides.csv.
# Run AFTER this:  python3 Context/normalize_footer.py   (footer + styles.css v16 + nav v7)
#                  python3 Context/blog-import/build_authors.py  (bylines + author pages + article.css v12)
#
#   python3 Context/blog-import/add_wayback_thoughtleaders.py
import os, re, json, html as _html
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "gen.py")).read())  # build(), render(), esc(); also sets ROOT
ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login"
BLOG = os.path.join(ROOT, "blog")

MONTHS = {m: i for i, m in enumerate(
    ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], 1)}

def fig(slug, f, alt, cap, w, h):
    cb = f'<figcaption>{cap}</figcaption>' if cap else ''
    return (f'        <figure class="article-figure"><img src="../../assets/images/{slug}/{f}" '
            f'width="{w}" height="{h}" alt="{esc(alt)}" loading="lazy" decoding="async">{cb}</figure>')

CTA_TALK = {'h3': 'Building for frontline impact?',
            'p': 'Talk with our team about designing digital tools that start small and scale sustainably.',
            'btntext': 'Get in touch', 'btnhref': '../../contact/index.html'}
CTA_CC = {'h3': 'See what CommCare can do for your program',
          'p': 'Talk with our team about digitizing service delivery and monitoring for your frontline workforce.',
          'btntext': 'Get in touch', 'btnhref': '../../contact/index.html'}

# ===================================================================== POSTS
posts = []

# ---- 1. Don't Prematurely Optimize Mobile Health (Jonathan Jackson, 2013) ----
posts.append(dict(
    slug="dont-prematurely-optimize-mobile-health",
    h1="Don&rsquo;t Prematurely Optimize Mobile Health",
    titletag="Don&rsquo;t Prematurely Optimize Mobile Health | Dimagi",
    ogtitle="Don't Prematurely Optimize Mobile Health",
    desc="A classic engineering warning, premature optimization is the root of all evil, applies just as well to mobile health: deciding what is truly critical to scale and sustainability before you invest your time and energy.",
    deck="A classic software-engineering warning applies just as well to mobile health: figure out what is truly critical to scale before you spend your energy optimizing it.",
    date="2013-03-20", datelabel="Mar 2013", author="Jonathan Jackson", initials="JJ",
    category="Reflections", crumb="Reflections", readtime="4 min read",
    cover="cover.jpg", coverw=1200, coverh=799,
    coveralt="A field team reviewing data together on phones and a tablet outdoors",
    covercaption="",
    ogimage="https://dimagi.com/assets/images/dont-prematurely-optimize-mobile-health/cover.jpg",
    ogw=1200, ogh=799, ogalt="A field team reviewing mobile data together",
    keywords="mobile health, mHealth, premature optimization, scale, sustainability, community health workers, CommCare, supervision, Donald Knuth, Dimagi",
    tags=["Dimagi", "Reflections"],
    toc=[["optimization-beyond-speed","Beyond speed"],["technology-amplifies-intent","Technology amplifies intent"],
         ["design-for-scale-early","Design for scale early"]],
    cta=CTA_TALK,
    related_slugs=["aligning-innovation-and-scale","can-we-scale-empathy","three-ways-to-achieve-economies-of-scale-in-mhealth"],
    body="""        <p class="lead">This piece grew out of an <a href="http://www.mhealthworkinggroup.org/" target="_blank" rel="noopener">mHealth working group</a> discussion in March 2013. Its argument is simple: in mobile health, as in software engineering, optimizing the wrong thing too early is a costly mistake.</p>

        <p>Professor Donald Knuth, a legend in the field of computer science, wrote a famous passage about premature optimization that will resonate with any technologist:</p>

        <blockquote>&ldquo;There is no doubt that the grail of efficiency leads to abuse. Programmers waste enormous amounts of time thinking about, or worrying about, the speed of noncritical parts of their programs, and these attempts at efficiency actually have a strong negative impact when debugging and maintenance are considered. We should forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil. Yet we should not pass up our opportunities in that critical 3%.&rdquo;</blockquote>

        <h2 id="optimization-beyond-speed">Optimization is not just about speed</h2>
        <p>This passage is usually cited in reference to performance and speed, but the same logic applies to scale and sustainability. The number of mHealth technologies is increasing, as is the maturity of certain platforms. Yet mHealth technology is mostly just an amplifier of human intentions. Deciding which &ldquo;parts of a program are really critical&rdquo; to scale and sustainability must be well understood before we can identify where to invest our time and energy.</p>

        <h2 id="technology-amplifies-intent">Technology amplifies human intent</h2>
        <p>In our work with community health workers (CHWs), we often struggle to determine how the performance improvement we are trying to achieve with systems like CommCare will actually be realized. This goes well beyond whether the technology is working, extending to human resources, ownership, and accountability. The motivation or management capacity may be lacking, and this is likely to be exacerbated at scale.</p>
        <p>Mobile technology cannot solve that on its own. If we are trying to better enable supervision and management, the cost of fixing the underlying HR or training issue may dwarf the entire cost of the mHealth technology. So if the return on investment of deploying the technology hinges on functioning supervision and management for the CHW system, then any optimization within the economics of the technology should not be addressed before the supervision and management issues are.</p>

        <h2 id="design-for-scale-early">But design for scale early</h2>
        <p>That said, designing for scale and sustainability early on is absolutely critical. If you do not proactively design pathways for optimization in certain areas, you may find them impossible or prohibitively expensive to improve later. Two design pathways worth leaving open:</p>
        <ol>
          <li><strong>Assume technology will change, and evolve with it.</strong> The pace of innovation is faster than we can imagine. Do not build only around today&rsquo;s technology, and do not be afraid to jump to new technologies when needed.</li>
          <li><strong>Build a positive feedback loop between the technology and the system.</strong> There is an old management saying that &ldquo;culture beats strategy,&rdquo; and culture can absolutely destroy technology. Even scalable technology will be a poor use of resources if it is introduced into a system that is not designed to use it. When good technology meets the right system dynamics, it improves the system, which generates more demand on the technology, and both get better together.</li>
        </ol>
""",
))

# ---- 2. Avoiding mHealth "Pilotitis" (Neal Lesh, 2013) ----
posts.append(dict(
    slug="avoiding-mhealth-pilotitis-doesnt-mean-you-shouldnt-start-small",
    h1="Avoiding mHealth &ldquo;Pilotitis&rdquo; Doesn&rsquo;t Mean You Shouldn&rsquo;t Start Small",
    titletag="Avoiding mHealth &ldquo;Pilotitis&rdquo; | Dimagi",
    ogtitle="Avoiding mHealth “Pilotitis” Doesn't Mean You Shouldn't Start Small",
    desc="Within mHealth, pilots have earned a bad name. But avoiding pilotitis does not mean you shouldn't start small. Dimagi CSO Neal Lesh on starting small in a way that is built to go big.",
    deck="Pilots have earned a bad name in mHealth. The answer is not to avoid starting small, but to start small in a way that is built to scale.",
    date="2013-12-12", datelabel="Dec 2013", author="Neal Lesh", initials="NL",
    category="Reflections", crumb="Reflections", readtime="5 min read",
    cover="cover.jpg", coverw=1200, coverh=800,
    coveralt="Children outside a home in a rural community where Dimagi works",
    covercaption="",
    ogimage="https://dimagi.com/assets/images/avoiding-mhealth-pilotitis-doesnt-mean-you-shouldnt-start-small/cover.jpg",
    ogw=1200, ogh=800, ogalt="A rural community where Dimagi works",
    keywords="mHealth, pilotitis, scale, frontline workers, CommCare, proof of concept, maternal health, ReMiND, Catholic Relief Services, USAID DIV, Neal Lesh, Dimagi",
    tags=["CommCare", "Reflections", "Maternal &amp; Newborn Health"],
    toc=[["start-small-go-big","Start small, go big"],["iteration-takes-time","Why iteration matters"],
         ["proof-of-concept","Proof-of-Concept packages"],["one-platform","One platform, built to scale"]],
    cta=CTA_CC,
    related_slugs=["three-ways-to-achieve-economies-of-scale-in-mhealth","aligning-innovation-and-scale","mobile-data-collection-figo"],
    body="""        <p class="lead">Within mHealth, pilots have earned a bad name, and for good reason. But avoiding &ldquo;pilotitis&rdquo; does not mean you should not start small. It means starting small in a way that is built to go big.</p>

        <p><em>This piece by Dimagi&rsquo;s Chief Strategy Officer, Neal Lesh, was originally featured on the Maternal Health Task Force&rsquo;s <a href="https://www.mhtf.org/" target="_blank" rel="noopener">Tech4MH blog</a>.</em></p>

        <h2 id="start-small-go-big">Making it easy to start small</h2>
        <p>Since 2008, Dimagi has helped organizations in 30 countries set up mobile projects with CommCare, an open-source mobile platform that supports frontline workers (FLWs). CommCare is actively used by over 130 frontline programs across numerous development sectors. One of the most common and compelling uses is to support FLWs delivering vital maternal health services: registering clients, tracking antenatal care visits, counseling on the importance of facility delivery, and calculating due dates. Thanks to support from USAID&rsquo;s Development Innovation Ventures, Dimagi will launch at least 40 new frontline programs in 2013 to use CommCare in India alone, a majority of them focused on maternal health.</p>
        <p>Technology is never the whole answer, but it can be an essential component of empowering FLWs and improving the maternal health services they offer. Our goal is to help frontline programs reach sustained impact at scale by making it as easy as possible to start small while being able to go big. Why start small? Within mHealth, pilots have gotten a bad name, given the many projects declared a success only because they started, regardless of whether they can or do continue. Indeed, many of our partners will tell us we can start with a small number of FLWs as long as we do not call it a pilot.</p>

        <h2 id="iteration-takes-time">Why iteration matters</h2>
        <p>mHealth applications, like most technology, take time and field iteration to develop. mHealth is still a young field, and iteration is necessary to develop usable systems. Organizational capacity to use mHealth takes time to develop too. Most organizations we work with do not fully appreciate what they are getting into until they have used CommCare for a while.</p>

        <h2 id="proof-of-concept">Proof-of-Concept packages</h2>
        <p>One way we make it easy to start small is by offering Proof of Concept (POC) packages, where funding allows, that include 10 free phones and about a month of remote and on-site support from Dimagi&rsquo;s experienced team. One thing that initially surprised us is how popular the POC packages are. To date, over 68 organizations in 18 countries have started using CommCare through POC packages. We receive a large number of applications when we put out requests for them, even from huge development organizations with budgets over 100 million dollars. We have come to realize that POC packages are popular because they remove much of the perceived risk for someone within an organization to initiate an mHealth project.</p>

        <h2 id="one-platform">One platform, built to scale</h2>
        <p>The key thing that allows us to start small but go big is that we offer CommCare as a Software-as-a-Service product hosted on our cloud server. All 130 frontline programs using CommCare run on the same platform. Anyone can create an account, develop their own CommCare application, or customize a pre-existing application from CommCare Exchange, the first open-source mHealth app store.</p>
        <p>One example is the Reducing Maternal and Newborn Deaths (ReMiND) pregnancy app developed by Catholic Relief Services (CRS) in partnership with Dimagi to support prenatal and postnatal care in the northern Indian state of Uttar Pradesh. Following initial testing and refining with 10 government-selected FLWs, the app scaled up to 271 FLWs, who use audio and visual prompts to systematically counsel and assess women and babies for danger signs. Supervisors are alerted when visits are missed, and the latest edition adds customized SMS reminders triggered by computer-detected newborn danger signs. The CRS site has become a strong innovation test bed and an increasingly well-known global example of mHealth as a supportive supervision tool.</p>
        <p>Over the following year, we expected to support CommCare and MOTECH Suite in several maternal health programs at large scale in India, Haiti, and other countries. In every case, we started small, and were very excited to go big.</p>
""",
))

# ---- 3. How Can We Leverage Technology to Bridge the Global Healthcare Divide? (JJ, 2016) ----
posts.append(dict(
    slug="how-can-we-leverage-technology-to-bridge-the-global-healthcare-divide",
    h1="How Can We Leverage Technology to Bridge the Global Healthcare Divide?",
    titletag="Leveraging Technology to Bridge the Global Healthcare Divide | Dimagi",
    ogtitle="How Can We Leverage Technology to Bridge the Global Healthcare Divide?",
    desc="Reflections from the 2016 World Economic Forum in Davos: with a 45x gap in healthcare spending between rich and poor countries, we need technology that shifts the focus from high-cost healthcare to low-cost health promotion.",
    deck="Reflections from Davos on a 45x gap in healthcare spending, and why bridging it means using technology to shift from high-cost healthcare to low-cost health promotion.",
    date="2016-02-01", datelabel="Feb 2016", author="Jonathan Jackson", initials="JJ",
    category="Reflections", crumb="Reflections", readtime="5 min read",
    cover="cover.jpg", coverw=1200, coverh=811,
    coveralt="Flags outside the World Economic Forum Annual Meeting in Davos, Switzerland",
    covercaption="The 2016 World Economic Forum Annual Meeting in Davos, Switzerland.",
    ogimage="https://dimagi.com/assets/images/how-can-we-leverage-technology-to-bridge-the-global-healthcare-divide/cover.jpg",
    ogw=1200, ogh=811, ogalt="The World Economic Forum Annual Meeting in Davos",
    keywords="global health, healthcare divide, World Economic Forum, Davos, health promotion, Ebola, malaria, GAVI, NCDs, low-cost technology, Dimagi, Jonathan Jackson",
    tags=["Dimagi", "Reflections"],
    toc=[["rebooting-healthcare","Rebooting healthcare"],["the-45x-divide","A 45x divide"],
         ["from-healthcare-to-health","From healthcare to health"],["the-economics","The economics of prevention"]],
    cta=CTA_TALK,
    related_slugs=["can-we-scale-empathy","problems-that-matter","a-more-just-inclusive-and-tolerant-world"],
    body="""        <p class="lead">I am just back from the <a href="https://www.weforum.org/" target="_blank" rel="noopener">2016 World Economic Forum Annual Meeting</a> in Davos, Switzerland, which I attended as part of the Schwab Foundation for Social Entrepreneurs. It was an amazing and overwhelming experience, and I came away more convinced than ever that we must focus innovation on the billions of people that advanced technology will never reach by market forces alone.</p>

        <h2 id="rebooting-healthcare">Rebooting healthcare at Davos</h2>
        <p>This year, the focus of the World Economic Forum was the Fourth Industrial Revolution and how the technology revolution is changing all aspects of our world. The effects are particularly profound in healthcare. I had the opportunity to discuss these changes in a session titled &ldquo;Rebooting Healthcare&rdquo; with Seth F. Berkley, chief executive officer of the GAVI Alliance; Jonathan Adiri, founder and chief executive officer of Healthy.io; and Elizabeth O&rsquo;Day, founder and chief executive officer of Olaris Therapeutics. Mr. Adiri shared how Healthy.io is using mobile phones as medical imaging devices, and Ms. O&rsquo;Day discussed how Olaris is developing precision medicines. These organizations are achieving remarkable results, and their contributions come at a critical moment for global health.</p>

        <h2 id="the-45x-divide">A 45x divide</h2>
        <p>According to 2013 data from the World Health Organization, average healthcare expenditure across all 54 member countries in Africa comes to about 200 dollars per person per year. By comparison, the United States spends roughly 9,000 dollars per person per year. This 45x difference in spending means that, for a vast portion of the world&rsquo;s population, we need to rethink our approach to healthcare. Many advanced technologies are simply too expensive to alleviate the health crisis for the billions for whom high-tech healthcare is out of reach. If we accept that this divide cannot be bridged with technology designed for a 9,000-dollar-a-year healthcare consumer, then we must find ways for technology to provide vastly lower-cost solutions to vastly more people.</p>

        <h2 id="from-healthcare-to-health">From healthcare to health promotion</h2>
        <p>One such solution is to use technology to shift our focus from healthcare to health promotion. We need to focus not only on precision healthcare but also on precision health: inexpensive solutions that automate health services and help foster ecosystems where communities can create their own. We saw the power of this approach during the Ebola epidemic. Rather than an expensive blockbuster drug or vaccine, rapid community mobilization facilitated by technology helped quell the outbreak. Simple mobile applications helped by giving communities information on preventative measures, including safe burials and how to conduct contact tracing. We must look for opportunities to replicate this success, using low-cost technology to ensure communities continue to have the preventative information that lets them keep themselves safe.</p>

        <h2 id="the-economics">The economics of prevention</h2>
        <p>Beyond better health outcomes, this shift from high-cost treatment to low-cost health promotion has serious economic implications. At a macro level, malaria has been estimated to cost Africa more than 12 billion dollars every year in lost GDP, roughly 1% of GDP, even though it could be controlled for a fraction of that sum. At an individual level, treating a child with malaria can cost the equivalent of half a month&rsquo;s average salary in Sierra Leone. Technology can help alleviate these costs by improving access to low-cost preventative measures such as bed nets.</p>
        <p>It was inspiring to learn about the precision technology in development at Davos, but I left more convinced than ever that we must also direct innovation toward the people these technologies will not reach. According to one BCG report, non-communicable diseases between now and 2030 are expected to cost five times the amount lost during the 2008 financial crisis. If we can collectively shift the market and the ecosystem to focus on health, not just healthcare, we can bring the creativity and innovation engine that knows no bounds to every person.</p>
""",
))

# ---- 4. Failing Fast: Does it apply to Healthcare? (Neal Lesh, 2017) ----
posts.append(dict(
    slug="failing-fast-does-it-apply-to-healthcare",
    h1="Failing Fast: Does it Apply to Healthcare?",
    titletag="Failing Fast: Does it Apply to Healthcare? | Dimagi",
    ogtitle="Failing Fast: Does it Apply to Healthcare?",
    desc="Technologists urge their public health colleagues to embrace failure and fail fast. After the 2017 SwitchPoint conference, Dimagi CSO Neal Lesh reflects on why that advice lands differently for the people caring for patients.",
    deck="Technologists love to fail fast. After SwitchPoint 2017, Dimagi CSO Neal Lesh reflects on why that advice lands very differently for the people caring for patients.",
    date="2017-05-05", datelabel="May 2017", author="Neal Lesh", initials="NL",
    category="Reflections", crumb="Reflections", readtime="5 min read",
    cover="cover.jpg", coverw=960, coverh=540,
    coveralt="A community gathering sitting together under a tree in a rural setting",
    covercaption="",
    ogimage="https://dimagi.com/assets/images/failing-fast-does-it-apply-to-healthcare/cover.jpg",
    ogw=960, ogh=540, ogalt="A community gathering under a tree",
    keywords="failing fast, healthcare, iteration, design under the mango tree, SwitchPoint, IntraHealth, continuous improvement, ICT4D, Neal Lesh, Dimagi",
    tags=["Dimagi", "Reflections"],
    toc=[["vulnerability","Vulnerability in the room"],["mango-tree","Design under the mango tree"],
         ["dont-fail-fast","A sudden realization"],["reframing","Reframing failure"]],
    cta=CTA_TALK,
    related_slugs=["problems-that-matter","aligning-innovation-and-scale","can-we-scale-empathy"],
    body="""        <p class="lead"><em>Dr. Neal Lesh, Chief Strategy Officer at Dimagi, shares his thoughts following the 2017 SwitchPoint Conference.</em></p>

        <p>I had the good fortune of attending and presenting at the 2017 <a href="https://www.switchpointideas.com/" target="_blank" rel="noopener">SwitchPoint</a> conference, organized by <a href="https://www.intrahealth.org/" target="_blank" rel="noopener">IntraHealth International</a>, in Saxapahaw, North Carolina. SwitchPoint brings together musicians, innovators, health practitioners, and a wide range of people working in global health and humanitarian response for a few days of information sharing and soul searching. The event is highly produced, and by putting people who do not typically work together in the same secluded space, and juxtaposing seemingly unrelated ideas, the meeting sparks creativity and self-reflection in the speakers as well as the attendees.</p>

        <figure class="article-figure"><img src="../../assets/images/failing-fast-does-it-apply-to-healthcare/img1.png" width="620" height="280" alt="The 2017 SwitchPoint conference" loading="lazy" decoding="async"><figcaption>The 2017 SwitchPoint conference, organized by IntraHealth International in Saxapahaw, North Carolina.</figcaption></figure>

        <h2 id="vulnerability">Vulnerability in the room</h2>
        <p>The word that best captures my experience is <strong>vulnerability</strong>. There was no jockeying to be seen as the smartest person in the room. Many people talked about mistakes or losses in their experience and how those events shaped their work. It is common for information technologists to urge our colleagues from public health and medicine to embrace failure. We know that the innovative things we build often do not work on the first try; we test them to see what breaks, and then fix the problems.</p>

        <h2 id="mango-tree">Design under the mango tree</h2>
        <p>We aspire to <strong>fail fast</strong> so we can move on to the next thing, which might work or might uncover a new set of problems to fix. In fact, if you are not failing at all, it means you are not trying enough new things, which means you will soon be obsolete. At Dimagi, we often speak about our &ldquo;design under the mango tree&rdquo; approach, which involves introducing technology in its early stages to real users, getting their feedback, and improving the technology based on it. We also promote continuous, incremental improvement once a system is launched, introducing new variations and testing which ones improve performance.</p>

        <h2 id="dont-fail-fast">A sudden realization</h2>
        <p>During SwitchPoint, I was moved to hear several health practitioners share stories of patients who had not survived despite their best efforts. In some cases there was a clear lesson or uplifting element; in others it was simply a formative moment. Listening to these stories, I had a sudden realization that now seems obvious:</p>
        <blockquote>I don&rsquo;t want my health providers to fail fast.</blockquote>
        <p>Similarly, I do not want a genius medical researcher to boast about having found a thousand ways not to cure a disease, even if that is what they must do to discover a cure. While learning from failure is essential in medicine and public health, each failure can be a profound loss.</p>

        <h2 id="reframing">Reframing failure for health systems</h2>
        <p>What I will take from SwitchPoint is a better understanding of why some of our partners may resist an iterative testing approach that inherently involves learning from failure. That resistance is often connected to their commitment and their training to provide the best possible care for each patient. At Dimagi, we will certainly continue our &ldquo;design under the mango tree&rdquo; and advocate for continuous improvement of digital systems through ongoing testing of new ideas. It is the only way we know to build a system that provides the most value to its users. But I will now work harder to incorporate this into a health-systems perspective, and to be more mindful of the stories of failure that most health workers carry with them.</p>
""",
))

# ---- 5. Casa Flor Ixcaco (Dimagi interview with Alana Marsili, 2016) ----
posts.append(dict(
    slug="casa-flor-ixcaco-commcare-guatemala-artisans",
    h1="Casa Flor Ixcaco: Using CommCare to Support Guatemalan Artisans",
    titletag="Casa Flor Ixcaco: CommCare for Guatemalan Artisans | Dimagi",
    ogtitle="Casa Flor Ixcaco: Using CommCare to Support Guatemalan Artisans",
    desc="Casa Flor Ixcaco is a cooperative of 20 indigenous female artisans in Guatemala. We spoke with Alana Marsili about building a CommCare app to bring point-of-sale data analytics to the women's weaving business.",
    deck="A cooperative of 20 indigenous female weavers in Guatemala turned to CommCare for point-of-sale data analytics. We spoke with Alana Marsili about how it came together.",
    date="2016-11-27", datelabel="Nov 2016", author="Dimagi", initials="D",
    category="CommCare", crumb="CommCare", readtime="5 min read",
    cover="cover.jpg", coverw=1200, coverh=589,
    coveralt="Two indigenous Guatemalan women in traditional dress holding a tablet running the CommCare app, with woven yarn behind them",
    covercaption="Artisans at Casa Flor Ixcaco use a CommCare app to capture point-of-sale data.",
    ogimage="https://dimagi.com/assets/images/casa-flor-ixcaco-commcare-guatemala-artisans/cover.jpg",
    ogw=1200, ogh=589, ogalt="Guatemalan artisans using the CommCare app on a tablet",
    keywords="Casa Flor Ixcaco, Guatemala, artisans, weaving, livelihoods, CommCare, case management, point of sale, data analytics, small enterprise, Dimagi",
    tags=["CommCare", "Case Study", "Livelihoods"],
    toc=[["the-need","Identifying the need"],["the-app","Building and rolling out the app"],
         ["the-goal","The goal, and advice for others"]],
    cta=CTA_CC,
    related_slugs=["five-talents-savings-groups","naatal-mbay-commcare-agricultural-support","taroworks-alternative-givedirectly-cash-transfer-case-study"],
    body="""        <p class="lead">Casa Flor Ixcaco is a small enterprise of 20 indigenous female artisans in Guatemala. We spoke with Alana Marsili, who worked with the cooperative to build a CommCare app that brought point-of-sale data analytics into their day-to-day business operations.</p>

""" + fig("casa-flor-ixcaco-commcare-guatemala-artisans", "img1.jpg",
          "Members of the Casa Flor Ixcaco weaving cooperative", "", 1000, 665) + """

        <p><em>Alana&rsquo;s graduate work at Georgetown posited that mobile applications could strengthen the relationships between small and medium domestic enterprises and formal institutions in Latin America, effectively creating a new middle class and tax base for the region. She found Dimagi&rsquo;s CommCare platform offered a chance to pilot that theory with a small enterprise in Guatemala.</em></p>

        <h2 id="the-need">Identifying the need</h2>
        <p><strong>How did you determine there was a technical need for Casa Flor Ixcaco?</strong></p>
        <p>Casa Flor Ixcaco, like many small enterprises, lacked access to a tool that could provide smart data analytics to transform business operations and enable a more sustainable approach to sales. It takes the women anywhere from one to four weeks to weave a product, which is sold in a market located three hours, a 30-minute boat ride, and a hike up the mountainside from Guatemala City. The market is isolated, but tourism and social media have opened unlikely inroads. Through the analytics we receive from CommCare, alongside website, Facebook, and Instagram analytics, we are positioning Casa Flor Ixcaco to maximize earnings from foot traffic and to create a virtual network of support and curated market opportunities based on data.</p>

        <h2 id="the-app">Building and rolling out the app</h2>
        <p><strong>What kind of app did you build for them?</strong></p>
        <p>I built a case management application that uses a form to ask five key questions to clients at the point of sale.</p>
        <p><strong>Who uses the app?</strong></p>
        <p>The application is built to be used by the client while a Casa Flor Ixcaco representative rings up the sale. Because their sales often come with busy tour groups on tight timelines, the goal is to capture 50% of sales data in a given week, and to enter the rest during down time.</p>
        <p><strong>Did you find app building to be a challenge? How about training the end users?</strong></p>
        <p>The application build was very easy. CommCare&rsquo;s platform is user friendly, and I found it easy to navigate the search functionality whenever I came across a challenge. Training was even easier. I explained the application to one of the employees, who was able to teach another employee on her own the next day.</p>

        <h2 id="the-goal">The goal, and advice for others</h2>
        <p><strong>What is the goal?</strong></p>
        <p>The goal is to streamline production, style, and the type of items in the store through a greater understanding of Casa Flor Ixcaco&rsquo;s consumer profile. We hope this information will let them work in additional market spaces with a clearer proposal to distributors, and help the women move from sustainability to profitability as more active players in their industry.</p>
        <p><strong>Any advice for similar organizations looking to incorporate a data collection tool?</strong></p>
        <p>We started by asking ourselves whether small changes could make a big difference, and then thought about how strengthening analytics at the point of sale could do that. Data is only helpful insofar as it is designed with an end goal in mind. We knew we had an end goal and we knew we needed data to make evidence-based decisions. I think this style of thinking can apply to any organization interested in exploring data collection.</p>

""" + fig("casa-flor-ixcaco-commcare-guatemala-artisans", "img2.jpg",
          "An artisan from the Casa Flor Ixcaco cooperative with woven textiles", "", 1000, 665) + """

        <p>You can follow the story and support the women by visiting <a href="https://www.woven-gt.com/" target="_blank" rel="noopener">woven-gt.com</a>.</p>
""",
))

# ---- 6. How FIGO Used Mobile Data Collection... (Dimagi, 2019) ----
posts.append(dict(
    slug="mobile-data-collection-figo",
    h1="How FIGO Used Mobile Data Collection to Improve Maternal Healthcare Across Six Countries",
    titletag="How FIGO Used Mobile Data Collection Across Six Countries | Dimagi",
    ogtitle="How FIGO Used Mobile Data Collection to Improve Maternal Healthcare Across Six Countries",
    desc="Roughly 214 million women want to avoid pregnancy but lack a modern method. Here is how FIGO used CommCare to track postpartum family planning across six countries and prove the approach worked.",
    deck="Roughly 214 million women want to avoid pregnancy but lack a modern method. Here is how FIGO used CommCare to track postpartum family planning across six countries.",
    date="2019-02-19", datelabel="Feb 2019", author="Dimagi", initials="D",
    category="CommCare", crumb="CommCare", readtime="6 min read",
    cover="cover.jpg", coverw=1200, coverh=900,
    coveralt="A FIGO team leads a training session for healthcare providers around a table",
    covercaption="A FIGO team leads a training on postpartum IUD insertion.",
    ogimage="https://dimagi.com/assets/images/mobile-data-collection-figo/cover.jpg",
    ogw=1200, ogh=900, ogalt="A FIGO maternal healthcare training session",
    keywords="FIGO, maternal health, family planning, postpartum IUD, PPIUD, contraception, CommCare, mobile data collection, monitoring and evaluation, Bangladesh, India, Kenya, Nepal, Tanzania, Sri Lanka, Dimagi",
    tags=["CommCare", "Case Study", "Maternal &amp; Newborn Health"],
    toc=[["an-unmet-need","An unmet need"],["a-new-approach","A new approach"],
         ["figo-takes-on-the-problem","FIGO takes on the problem"],
         ["using-mobile-data-collection","Using mobile data collection"],["a-successful-project","A successful project"]],
    cta=CTA_CC,
    related_slugs=["avoiding-mhealth-pilotitis-doesnt-mean-you-shouldnt-start-small","strengthening-mental-health-services-with-digital-solutions","mobile-data-collection-nutrition","abt-associates-vectorlink-malaria-control"],
    body="""        <p class="lead">There are roughly 214 million women of reproductive age in low-income regions who want to avoid pregnancy but have no modern way to do so. Here is how the International Federation of Gynecology and Obstetrics (FIGO) used CommCare to bring postpartum family planning to women across six countries, and proved that it worked.</p>

        <h2 id="an-unmet-need">An unmet need</h2>
        <p>As soon as a woman gives birth, her odds of an unintended pregnancy increase, presenting new challenges for her and her child. Dr. Anita Makins, PPIUD Project Director at FIGO, explains:</p>
        <blockquote>&ldquo;Globally, there are 214 million women with an unmet need for contraception. This signals a disconnect between a woman&rsquo;s desire to plan her pregnancies and her ability to do so. Unmet need can lead to shorter birth-spacing, which has a negative impact on both maternal and newborn health, and can put additional economic strain on a family, perpetuating the poverty cycle.&rdquo;</blockquote>

        <h2 id="a-new-approach">A new approach</h2>
        <p>A reliable contraceptive method gives a woman control, and with it the opportunity to look after her new family, both in terms of care for her newborn and economic productivity. Effective methods of contraception have been proven to improve maternal health and reduce maternal mortality. This is why FIGO sought a way to provide affordable, long-acting, reversible contraception to millions of women. When they settled on an intrauterine device (IUD), they wanted to make it as effective as possible, and found that a particular method and set of tools, long curved Kelly forceps, would reduce what was perceived to be a high expulsion rate.</p>

        <h2 id="figo-takes-on-the-problem">FIGO takes on the problem</h2>
        <p>FIGO received funding to introduce the practice to six hospitals in Sri Lanka. After initial success, it expanded to an additional 12 hospitals in Sri Lanka and six hospitals in each of five more countries: Bangladesh, India, Kenya, Nepal, and Tanzania. The goal was to address the gap in the continuum of maternal health care by increasing the capacity of healthcare professionals to offer IUDs, training community midwives, health workers, doctors, and delivery unit staff.</p>
        <p>One key problem was that IUDs did not necessarily have the best reputation. Whether the reason was religious, cultural, or based on a poor prior experience, FIGO knew this was an obstacle. Their answer was to tackle bias at the provider level through training and sensitization, and to raise awareness by counseling women on all aspects of postpartum family planning. In some countries, this meant working with community health workers to educate women who were delivering, as well as the wider community.</p>

""" + fig("mobile-data-collection-figo", "img1.jpg",
          "A community health worker uses a mobile data collection app to interview a recent mother",
          "A community health worker uses CommCare to interview a recent mother.", 1000, 665) + """

        <h2 id="using-mobile-data-collection">Using mobile data collection</h2>
        <p>As part of the research, FIGO hired data collection officers in each country to collect data on every woman delivering in the participating hospitals. Using CommCare, they tracked counseling, consent, postpartum intrauterine devices (PPIUDs), and follow-up to assess the acceptability, cost-effectiveness, and outcomes of the effort. Emily Tunnacliffe, PPIUD Project Manager at FIGO, explained:</p>
        <blockquote>&ldquo;CommCare provided a unique platform in that they have a global presence, with hubs in some of our project countries. They were able to provide on-hand support and training where needed, giving our country teams ownership of data collection in their particular contexts.&rdquo;</blockquote>
        <p>To track as many patients as possible, FIGO set up follow-ups for each registered case at six weeks and six months, with an 18-month follow-up scheduled, including provider surveys, in-depth interviews, and hospital checklists. After the first year, FIGO was able to track 75% of women delivering in the participating facilities, regardless of their PPIUD status. With data on patients&rsquo; knowledge of PPIUDs, consent, insertion, and complication rates, FIGO was able to convince a wider audience in each of the six countries that PPIUDs are a useful and effective method of postpartum contraception. The data also gave clinicians clearer ways to identify problems, train and support individual providers, and improve the insertion method.</p>

        <h2 id="a-successful-project">A successful project</h2>
        <p>FIGO&rsquo;s PPIUD project faced more challenges than this short summary can capture, but in the end the team was able to provide women across Africa and South Asia with stability during a period of their lives that should be empowering, not debilitating. In this instance, mobile data collection was not used to reinforce protocols or run trainings; the clinicians, community midwives, health workers, doctors, and delivery unit staff were ultimately responsible for the program&rsquo;s success. But the monitoring and evaluation done on the initiative both improved that process and provided proof for additional regions to help the hundreds of millions of women who could still benefit from an effective postpartum contraceptive.</p>
        <p>For more on FIGO&rsquo;s PPIUD initiative, and the source for much of the information referenced here, see the <a href="https://obgyn.onlinelibrary.wiley.com/doi/10.1002/ijgo.12598" target="_blank" rel="noopener">published study</a>.</p>
""",
))

# ---- 7. Using CommCare to Track Gang Violence in Cape Town (The Safety Lab, 2013) ----
posts.append(dict(
    slug="tracking-gang-violence-with-commcare",
    h1="Using CommCare to Track Gang Violence in Cape Town",
    titletag="Using CommCare to Track Gang Violence in Cape Town | Dimagi",
    ogtitle="Using CommCare to Track Gang Violence in Cape Town",
    desc="In Hanover Park, one of Cape Town's most gang-affected communities, the CeaseFire project uses CommCare to capture data on evolving violence trends so field workers can predict, and try to prevent, the next shooting.",
    deck="In Hanover Park, one of Cape Town's most gang-affected communities, the CeaseFire project uses CommCare to capture violence trends so field workers can help prevent the next shooting.",
    date="2013-12-06", datelabel="Dec 2013", author="The Safety Lab", initials="TS",
    category="CommCare", crumb="CommCare", readtime="5 min read",
    cover="cover.jpg", coverw=1235, coverh=823,
    coveralt="A community street scene in South Africa",
    covercaption="",
    ogimage="https://dimagi.com/assets/images/tracking-gang-violence-with-commcare/cover.jpg",
    ogw=1235, ogh=823, ogalt="A community street scene in South Africa",
    keywords="CommCare, gang violence, Cape Town, Hanover Park, CeaseFire, Safety Lab, violence prevention, mobile data collection, South Africa, service delivery, Dimagi",
    tags=["CommCare", "Case Study", "Service Delivery"],
    toc=[["ceasefire-hanover-park","CeaseFire Hanover Park"],["why-trend-data-matters","Why trend data matters"],
         ["the-problem-with-paper","The problem with paper"],["how-commcare-helps","How CommCare helps"]],
    cta=CTA_CC,
    related_slugs=["ndoh-national-scale-mhealth-south-africa","adpp-mozambique-tb-local-response","mhp-salud-integrated-community-health"],
    body="""        <p class="lead">In an effort to reduce gang-based violence and murder in one of Cape Town&rsquo;s most gang-affected communities, the CeaseFire Hanover Park project launched in late 2012. Using Dimagi&rsquo;s CommCare platform, the Safety Lab built a system for CeaseFire to capture data on evolving trends in gang violence more efficiently, so the program can better predict, and try to prevent, the next attack.</p>

        <h2 id="ceasefire-hanover-park">CeaseFire Hanover Park</h2>
        <p>CeaseFire Hanover Park is a gang-violence intervention and prevention program in a Cape Town community plagued by high levels of gang-related violence. In 2012 and 2013, the year the program launched, the police precinct in which Hanover Park sits recorded 71 murders for an area of 53,911 people, 34,625 of whom live in Hanover Park. The program seeks to reduce violence by training and deploying field workers who act as outreach workers and &ldquo;violence interrupters.&rdquo; Most are reformed ex-gang members trained to mediate conflicts between gangs on the streets before they turn violent. The system has also freed field workers to focus on intervention and prevention work rather than spending countless hours on paper-based logistics in the office.</p>

        <h2 id="why-trend-data-matters">Why trend data matters</h2>
        <p>Detecting and interrupting planned violence is a key component of CeaseFire, and it relies on accurate, up-to-date trend data. An area that experiences a sudden increase in threats of violence is more likely to see a future increase in attempted murders; an area with a spike in attempted murders is more likely to see a rise in actual murders. To prevent this escalation, CeaseFire increases the number of field workers in an identified risk area to help mitigate conflict and reduce the likelihood of a gang-related murder.</p>

        <h2 id="the-problem-with-paper">The problem with paper</h2>
        <p>Previously, data collection was done on paper forms that required outreach workers to fill in paperwork daily, case by case, from a remote office. Once completed and filed, the forms had to be recorded on a spreadsheet and plotted on a map before trends could be spotted and acted upon. The system only works at maximum impact if data is recorded accurately, consistently, and promptly. The street is an inopportune place to do paperwork: carrying a clipboard can compromise field workers&rsquo; mediation work by undermining the trust they have with the community. As a result, the paper-based system demanded that field workers spend significant time in the office, exactly when periods of high violence required them on the streets.</p>
        <p>Before CommCare, CeaseFire Hanover Park had significant problems with its violence-prediction system. Completed forms piled up waiting to be captured because active presence on the street took priority during times of high violence. Field workers also submitted forms late, often many days after an event, creating a lag that reduced the accuracy of the data, the longer the gap between an event and its recording, the less fresh it was in their minds.</p>

""" + fig("tracking-gang-violence-with-commcare", "chart.png",
          "A visualization of violence trend data captured through the CommCare system",
          "Trend data captured in CommCare helps the team anticipate where violence may escalate.", 778, 722) + """

        <h2 id="how-commcare-helps">How CommCare helps</h2>
        <p>To streamline data collection, a CommCare app was developed featuring the five forms most commonly used by field workers to record violence-prevention interventions, threats of violence, high-risk individuals, and the time and location of shootings. Paper forms tend to be long, and their heavy reliance on text is less effective than the combination of text and simple symbols that the CommCare tool allows. Simple icons were developed for each question, so that once a field worker is acquainted with the forms, completing them is greatly expedited. The app was deployed on Android devices for a simple interface that resonates with field workers&rsquo; comfort using their own mobile phones. The CommCare app has helped to:</p>
        <ul>
          <li>Streamline and enhance the efficiency of the data-capture process.</li>
          <li>Incentivize field workers to relay information shortly after an event occurs.</li>
          <li>Increase the ease of filling in forms and the accuracy of the information captured.</li>
          <li>Make data on the real-time situation on the street immediately accessible.</li>
        </ul>
        <p><em>About the author: Douglas is a researcher at The Safety Lab, an innovation hub and test centre based in the Western Cape province of South Africa that aims to catalyse social innovation and develop effective, street-ready safety solutions.</em></p>
""",
))

# ===================================================================== LISTING
idx_fp = os.path.join(BLOG, "index.html")
S = open(idx_fp, encoding='utf-8').read()
card_re = re.compile(r'<article class="blog-card".*?</article>', re.S)
existing = card_re.findall(S)

def card_slug(c):
    m = re.search(r'href="([^"/]+)/index\.html"', c); return m.group(1) if m else None
def card_date_key(c):
    m = re.search(r'class="blog-card-date">([A-Z][a-z]{2}) (\d{4})<', c)
    return (int(m.group(2)), MONTHS.get(m.group(1), 0)) if m else (0, 0)
listing = {card_slug(c): c for c in existing}

# related-card builder pulls real title/img/date from the live listing cards
def related_from_listing(slugs):
    out = []
    for s in slugs:
        c = listing.get(s)
        if not c:
            continue
        title = re.search(r'class="blog-card-title">(.*?)</h2>', c, re.S).group(1).strip()
        img = re.search(r'class="blog-card-image"[^>]*>\s*<img src="([^"]+)"', c, re.S).group(1).replace("../assets/", "../../assets/")
        date = re.search(r'class="blog-card-date">(.*?)</span>', c).group(1).strip()
        prod = re.search(r'data-product="([^"]*)"', c).group(1)
        typ = re.search(r'data-type="([^"]*)"', c)
        cat = prod if prod and prod != "None" else (typ.group(1) if typ else "Dimagi")
        out.append(dict(href=f"../{s}/index.html", img=img, w=1200, h=750,
                        cat=cat, title=title, date=date, alt=re.sub('<[^>]+>', '', title)))
        if len(out) == 3:
            break
    return out

# per-post listing taxonomy: (data-product, data-type, data-topic, data-country, data-sector)
TAX = {
 "dont-prematurely-optimize-mobile-health":            ("None", "Reflections", "Dimagi", "None", "None"),
 "avoiding-mhealth-pilotitis-doesnt-mean-you-shouldnt-start-small": ("CommCare", "Reflections", "Dimagi", "Multiple countries", "Maternal &amp; Newborn Health"),
 "how-can-we-leverage-technology-to-bridge-the-global-healthcare-divide": ("None", "Reflections", "Dimagi", "None", "None"),
 "failing-fast-does-it-apply-to-healthcare":           ("None", "Reflections", "Dimagi", "None", "None"),
 "casa-flor-ixcaco-commcare-guatemala-artisans":       ("CommCare", "Case Study", "None", "Latin America", "Livelihoods"),
 "mobile-data-collection-figo":                        ("CommCare", "Case Study", "None", "Multiple countries", "Maternal &amp; Newborn Health"),
 "tracking-gang-violence-with-commcare":               ("CommCare", "Case Study", "None", "Africa", "Service Delivery"),
}

def new_card(p):
    prod, typ, topic, country, sector = TAX[p['slug']]
    img = f"../assets/images/{p['slug']}/{p['cover']}"
    href = f"{p['slug']}/index.html"
    alt = re.sub('<[^>]+>', '', p['h1'])
    return (
f' <article class="blog-card" data-product="{prod}" data-type="{typ}" data-topic="{topic}" data-country="{country}" data-sector="{sector}">\n'
f' <a class="blog-card-image" href="{href}">\n'
f' <img src="{img}" alt="{esc(alt)}" loading="lazy" decoding="async">\n'
f' </a>\n'
f' <div class="blog-card-body">\n'
f' <h2 class="blog-card-title">{p["h1"]}</h2>\n'
f' <p class="blog-card-desc">{esc(p["desc"])}</p>\n'
f' <div class="blog-card-footer">\n'
f' <span class="blog-card-date">{p["datelabel"]}</span>\n'
f' <a class="blog-card-link" href="{href}">Read more</a>\n'
f' </div>\n'
f' </div>\n'
f' </article>')

# attach related now that listing is parsed
for p in posts:
    p['related'] = related_from_listing(p['related_slugs'])

# render WITH related (build() needs p['related'])
for p in posts:
    p2 = dict(p); p2['toc'] = [tuple(x) for x in p['toc']]
    os.makedirs(os.path.join(BLOG, p['slug']), exist_ok=True)
    open(os.path.join(BLOG, p['slug'], "index.html"), "w", encoding='utf-8').write(build(p2))
    print("rendered", p['slug'])

new_slugs = {p['slug'] for p in posts}
cards = [c for c in existing if card_slug(c) not in new_slugs]
cards += [new_card(p) for p in posts]
cards.sort(key=card_date_key, reverse=True)
grid_inner = "\n".join(cards)

g0 = S.index('<div class="blog-grid">'); g0e = S.index('>', g0) + 1
gm = S.index('<div class="blog-more"', g0e); gm_line = S.rfind('\n', 0, gm) + 1
open(idx_fp, "w", encoding='utf-8').write(S[:g0e] + "\n" + grid_inner + "\n      " + S[gm_line:])
print(f"listing rebuilt: {len(cards)} cards (+{len(posts)})")

# ===================================================================== tag_overrides
to_fp = os.path.join(HERE, "tag_overrides.csv")
to = open(to_fp, encoding='utf-8').read()
SECTOR_PLAIN = {"Maternal &amp; Newborn Health": "Maternal & Newborn Health"}
for p in posts:
    if p['slug'] in to:
        continue
    _, _, _, country, sector = TAX[p['slug']]
    sec = SECTOR_PLAIN.get(sector, sector)
    sec = "" if sec == "None" else sec
    ctry = "" if country == "None" else country
    if not to.endswith("\n"):
        to += "\n"
    to += f'{p["slug"]},{ctry},{sec},,"Wayback restore {p["datelabel"]}; deleted post recovered from WP export"\n'
open(to_fp, "w", encoding='utf-8').write(to)
print("tag_overrides updated")

# ===================================================================== sitemap
sm_fp = os.path.join(ROOT, "sitemap.xml")
sm = open(sm_fp, encoding='utf-8').read()
sample = re.search(r'<loc>([^<]*aligning-innovation-and-scale[^<]*)</loc>', sm)
for p in posts:
    if p['slug'] in sm:
        continue
    url = sample.group(1).replace("aligning-innovation-and-scale", p['slug']) if sample else f"https://dimagi.com/{p['slug']}/"
    entry = f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{p['date']}</lastmod>\n    <changefreq>yearly</changefreq>\n    <priority>0.6</priority>\n  </url>\n"
    sm = sm.replace("</urlset>", entry + "</urlset>")
open(sm_fp, "w", encoding='utf-8').write(sm)
print("sitemap updated")
print("DONE")
