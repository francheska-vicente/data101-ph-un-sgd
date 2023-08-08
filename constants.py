sdg_linechart_desc_default = "Choose an indicator to track its progress over the years."
sdg_barchart_desc_default = "Choose an indicator to compare its progress between all regions for the latest year."
sdg_choropleth_desc_default = "Choose an indicator to visualize its value on the Philippine map."

sdg_linechart_desc = "This linechart provides a visual representation of the selected indicator's trend over the years, represented by the blue line. The red line (if available) signifies the target goal for the indicator; closer proximity between the blue and red data points indicates better progress for the specific year."
sdg_linechart_tip = "Click on a data point to see the information for that specific year on all the graphs."
sdg_barchart_desc = "This barchart allows you to compare the progress of the chosen indicator between regions for a specific year. Each bar represents a region, and its length corresponds to the value of the indicator for that region."
sdg_barchart_tip = (
    "Click on the bars to toggle the arrangement between ascending and descending."
)

sdg_choropleth_desc1 = "This choropleth colors the regions based on the value of the indicator chosen. With this, it would easily show which regions have lower value compared to the other regions."
sdg_choropleth_desc2 = "This choropleth colors the regions based on the value of the correlation of the two chosen indicators."
sdg_choropleth_tip2 = "Click on a region to see the information for that specific region on the lines and bar chart."

reg_linechart_desc = "This line chart allows you to see the trend of all of the indicators under a specific target and determine which indicators would need to be improved. "
reg_linechart_tip = "Click on a data point to see the information for that specific year on the choropleth map."
reg_heatmap_desc = "This heat map illustrates how different targets of the SDG are related to each other. It indicates whether the two targets are moving in the same direction (positive value) or in opposite directions (negative value) based on the data available."
reg_choropleth_desc = "This choropleth map shows the area (in km^2) of each of the regions."
reg_choropleth_tip = "Click on a region to see the information for that specific region on the line charts."

blank_chart = {
    "layout": {
        "xaxis": {"visible": False},
        "yaxis": {"visible": False},
        "annotations": [
            {
                "text": "No input yet",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 28},
            }
        ],
    }
}

no_data_chart = {
    "layout": {
        "xaxis": {"visible": False},
        "yaxis": {"visible": False},
        "annotations": [
            {
                "text": "No matching data found",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 28},
            }
        ],
    }
}

targets_value = [
    "Target Number",
    "",
    "1.2.",
    "1.4.",
    "1.4.",
    "1.4.",
    "1.4.",
    "1.4.",
    "1.4.",
    "1.4.",
    "1.4.",
    "1.4.",
    "1.5.",
    "3.4.",
    "3.4.",
    "3.4.",
    "3.4.",
    "3.4.",
    "3.7.",
    "3.7.",
    "4.1.",
    "4.1.",
    "4.1.",
    "4.1.",
    "4.1.",
    "4.1.",
    "4.1.",
    "4.1.",
    "4.1.",
    "",
    "7.1.",
    "8.1.",
    "10.1.",
    "10.1.",
    "14.5.",
    "14.5.",
    "16.1.",
    "16.1.",
]

target_info = [
    "The proportion of poverty should be halved.",
    "Ensure equal rights to economic resources.",
    "Enhance resilience of vulnerable individuals to climate and other shocks.",
    "Ensure income growth for the bottom 40%.",
    "Conserve 10% of coastal and marine areas.",
    "Reduce global violence and death rates.",
    "Reduce non-communicable disease mortality.",
    "Ensure sexual and reproductive healthcare.",
    "Achieve quality education for all.",
    "Ensure universal access to energy services.",
    "Promote sustained economic growth for all.",
]

goals_information = [
    [
        "The objective of eradicating extreme poverty for every individual worldwide by 2030 is a crucial aspect of the 2030 Agenda for Sustainable Development.",
        "From 2015 to 2018, there was a continuous decline in global poverty, with the poverty rate dropping from 10.1 percent to 8.6 percent. However, recent estimations indicate that due to the impact of the COVID-19 pandemic, the global poverty rate experienced a significant rise from 8.3 percent in 2019 to 9.2 percent in 2020. This increase marks the first instance of extreme poverty escalating since 1998 and represents the largest setback to poverty reduction since 1990. As a result, progress in reducing poverty has been pushed back by approximately three years. Currently, the projected poverty rate of the Philippines by 2030 is 7%%, which fails to achieve the goal of this SDG.",
    ],
    [
        "This focuses on  creating a world free of hunger by achieving food security, improving nutrition, and promoting sustainable agriculture practices. Prior to the emergence of the COVID-19 pandemic, there had been a steady increase in the population experiencing hunger and food insecurity from 2014 onwards.",
        "However, the COVID-19 crisis has further elevated these already rising rates and intensified all types of malnutrition, particularly among children. Additionally, the ongoing conflict in the Ukrain-Russia war is causing significant disruptions to global food supply chains, resulting in the most severe global food crisis since the Second World War.",
    ],
    [
        "The third SDG ensures healthy lives for all and promotes well-being for all ages. With the emergence of COVID-19, this now includes the vaccination of all. The pandemic has underscored the necessity of enhancing global health security systems to effectively prevent and respond to future pandemics. Addressing these challenges and resolving longstanding deficiencies in healthcare delivery calls for immediate action in fortifying health systems, such as providing a stronger universal healthcare for everyone."
    ],
    [
        "This SDG entails that quality education is inclusive and equitable and lifelong learning opportunities are promoted. Ensuring universal access to quality education is essential for establishing a peaceful and prosperous global society. Education equips individuals with the necessary knowledge and skills to maintain good health, secure employment, and promote tolerance."
    ],
    [
        "This SDG focuses on ending discrimination against women and girls. Empowering them has proven to foster economic growth and progress. The UNDP has made gender equality a priority, leading to significant progress in education, with increased female enrollment and improved gender parity in primary education in most regions.",
        "Challenges persist, including labor market inequalities, sexual violence, unequal distribution of unpaid care work, and discrimination in public office. Achieving gender equality requires granting women equal rights to land, property, sexual and reproductive health, and access to technology.",
    ],
    [
        "The 6th SDG stresses the importance of access to safe water, sanitation, and hygiene for human well-being. Billions may lack these services by 2030 without accelerated progress. Growing water demand due to population growth, urbanization, and various sectors poses challenges. Misuse, poor management, and contamination worsen water stress. To achieve universal access by 2030, progress must quadruple, potentially saving 829,000 lives annually from water-related diseases."
    ],
    [
        "By 2030, the Sustainable Development Goal 7 (SDG 7) seeks to guarantee that everyone has access to cheap, dependable, and clean energy. Progress was achieved between 2000 and 2018, with a rise in availability of electricity from 78%% to 90%% and a decline in the number of those without it.",
        "However, investments in renewable energy sources like solar, wind, and thermal power are urgently needed due to the expanding world population and the need for affordable energy. To combat climate change and promote sustainable development, achieving SDG 7 necessitates boosting the use of renewable energy sources, providing equal energy access globally, and increasing clean energy infrastructure.",
    ],
    [
        "The primary objective of the eighth SDG is to achieve full and productive employment, promote sustained economic growth, higher productivity, and technological innovation, while also addressing the issues of forced labor, slavery, and human trafficking. It aims to significantly reduce global unemployment, particularly in the face of slower economic growth and widening inequalities, ensuring that decent work opportunities are available to all men and women by the year 2030."
    ],
    [
        "The ninth SDG aims to advance sustainable economic development and growth via investments in technology, innovation, and infrastructure. Since a large majority of the world's population lives in cities, upgrading mass transit and implementing renewable energy sources are priorities.",
        "To address economic and environmental concerns, generate new employment possibilities, and improve energy efficiency, it is crucial to promote the expansion of new sectors and information technology. In addition, the SDG seeks to close the digital gap, especially in developing nations, by granting everyone access to the Internet and encouraging entrepreneurship and innovation via access to knowledge and information.",
    ],
    [
        "The tenth SDG aims to reduce global economic disparity, addressing the imbalanced income distribution, particularly with the richest 10%% holding a significant share while the poorest 10%% struggle with little income.",
        "Effective policies promoting economic inclusion regardless of gender or ethnicity are crucial, along with global solutions like improved financial market regulation, increased development aid, and targeted foreign direct investment. Facilitating safe mobility also plays a key role in achieving the goal of reducing income inequality worldwide.",
    ],
    [
        "The eleventh SDG aims to achieve sustainable urban development amidst the continuous global urbanization. By 2050, two-thirds of the world's population is projected to live in cities, requiring significant changes in urban planning and management.",
        "The rise of mega-cities, especially in developing regions, driven by population growth and migration, has led to increased slums, emphasizing the urgency of sustainable development. To create sustainable cities, investments in public transportation, green spaces, and inclusive urban design are essential, promoting job opportunities, affordable housing, and resilient communities. These efforts will enhance the sustainability and livability of urban areas for present and future generations.",
    ],
    [
        "To achieve economic growth and sustainable development, it is imperative to reduce our ecological footprint by transforming how we produce and consume goods and resources - that is the goal of the twelveth SDG. ",
        "Addressing water usage in agriculture and managing natural resources efficiently are essential targets. Promoting recycling and waste reduction in industries, businesses, and among consumers is crucial, along with supporting developing countries in adopting sustainable consumption patterns by 2030. Additionally, reducing global food waste at the retailer and consumer levels is vital to create more efficient production and supply chains, enhancing food security and advancing toward a resource-efficient economy.",
    ],
    [
        "The objective of the thirteenth SDG is to tackle climate change by reducing greenhouse gas emissions and addressing its drastic effects. Mobilizing funds of US$100 billion annually by 2020 to support developing countries in adapting to climate change and promoting low-carbon development is crucial.",
        "Supporting vulnerable regions aligns not only with Goal 13 but also with other SDGs. Integration of disaster risk measures, sustainable resource management, and human security into national development strategies is essential. Despite challenges, limiting global temperature rise to 1.5°C or 2°C above pre-industrial levels is achievable through strong political will, increased investment, and existing technology, requiring urgent and ambitious collective action.",
    ],
    [
        "The goal of the fourteenth SDG is to sustainably manage and protect the world's oceans and coastal ecosystems to counterbalance climate change. Over three billion people depend on marine biodiversity for their livelihoods, but 30 percent of fish stocks are overexploited.",
        "Oceans absorb 30 percent of human-produced carbon dioxide, leading to a 26 percent rise in ocean acidification since the industrial revolution. Marine pollution, primarily from land-based sources, has reached alarming levels, with 13,000 pieces of plastic litter per square kilometer of ocean. The SDGs aim to tackle these challenges through international law, conservation, and sustainable use of ocean-based resources.",
    ],
    [
        "SDG 15 aims to preserve and protect the earth and ocean, crucial for human sustenance and livelihoods. With plant life providing 80 percent of our diet and forests serving as vital habitats for countless species, urgent action is needed to combat deforestation and degradation of drylands.",
        "Preserving biodiversity is essential, as thousands of animal and plant species are illegally traded, leading to insecurity, conflict, and corruption. Safeguarding natural habitats and biodiversity supports global food and water security, climate change mitigation and adaptation, and peace and security.",
    ],
    [
        "The sixteenth SDG aspires to achieve sustainable development by prioritizing peace, stability, human rights, and effective governance based on the rule of law. Addressing disparities in our world, where some regions thrive while others suffer cycles of conflict and violence, is essential. Armed violence and insecurity hinder economic growth and perpetuate grievances.",
        "To realize the Sustainable Development Goals, concerted efforts are needed to significantly reduce all forms of violence, collaborate with governments and communities to end conflicts, and promote the rule of law and human rights. Empowering developing countries' engagement in global governance institutions is also critical for fostering lasting peace, human dignity, and sustainable development worldwide.",
    ],
    [
        "SDG 17 seeks to promote sustainable development through strong global partnerships and cooperation. This involves addressing the shortfall in Official Development Assistance (ODA) and providing more aid to handle humanitarian crises effectively.",
        "Additionally, improving access to technology and knowledge-sharing is crucial for fostering innovation and sustainable growth. Coordinating debt management policies and encouraging investments in least developed regions are vital steps towards achieving the SDGs. Enhanced cooperation between North-South and South-South regions, along with fair international trade, play a significant role in ensuring universal benefits and successful accomplishment of the SDGs.",
    ],
]

goals_desc = [
    "End poverty in all its forms everywhere.",
    "End hunger, achieve food security and improved nutrition and promote sustainable agriculture.",
    "Ensure healthy lives and promote well-being for all at all ages.",
    "Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all.",
    "Achieve gender equality and empower all women and girls.",
    "Ensure availability and sustainable management of water and sanitation for all.",
    "Ensure access to affordable, reliable, sustainable and modern energy for all.",
    "Promote sustained, inclusive and sustainable economic growth.",
    "Build resilient infrastructure and promote inclusive and sustainable industrialization.",
    "Reduce inequality within and among countries.",
    "Make cities and human settlements inclusive, safe, resilient and sustainable.",
    "Ensure sustainable consumption and production patterns.",
    "Take urgent action to combat climate change and its impacts.",
    "Conserve and sustainably use the oceans, seas and marine resources for sustainable development.",
    "Protect, restore and promote sustainable use of terrestrial ecosystems.",
    "Promote peaceful and inclusive societies for sustainable development.",
    "Strengthen the means of implementation and revitalize the Global Partnership for Sustainable Development.",
]

region_images = [
    "region1.jpg",
    "region2.jpg",
    "region3.jpg",
    "region4a.jpg",
    "mimaropa.jpg",
    "region5.jpg",
    "region6.jpg",
    "region7.jpg",
    "region8.jpg",
    "region9.jpg",
    "region10.jpg",
    "region11.jpg",
    "region12.jpg",
    "caraga.jpg",
    "ncr.jpg",
    "car.jpg",
    "barmm.jpg",
]
