import random

kind_map = {
    "Herbaceous": 0,
    "Wood": 1
}

mois_map = {
    "Dry": lambda: random.randint(0, 35),
    "Moist": lambda: random.randint(35, 65),
    "Wet": lambda: random.randint(75, 100)
}

soil_map = {
    "Sand": 0.5,
    "Alluvium": 1.1,
    "Loam": 2,
    "Clay": 3
}

stage_map = {
    "Germination": 1, #_____________--
    "Growing": 1, 
    "Full-growing": 2
}

CNN_map_title = {
    0: 'Amaranth (Rau dền)\n', 
    1: 'Apple (Táo)\n', 
    2: 'Cabbage (Bắp cải)\n', 
    3: 'Crown_daisy (Cải cúc)\n', 
    4: 'Cucumber (Dưa leo)\n',
    5: 'Lettuce (Xà lách)\n', 
    6: 'Orange (Cam)\n',
    7: 'Spring_onion (Hành lá)\n',
    8: 'Tomato (Cà chua)\n', 
    9: 'Water_spinach (Rau muống)\n'
}

CNN_map_content = {
    0: (
        "1. Health benefits:\n", 
        "Amaranth leaves contain a high amount of antioxidants, vitamin A, vitamin C, and fiber, which help boost the immune system. Additionally, they provide folic acid and potassium, which may support cardiovascular health and the nervous system.\n\n", 
        "2. Suitable for cultivation in:\n", 
        "Amaranth leaves are suitable for cultivation in various geographical regions and climates. The soil for growing amaranth should be rich in organic matter, loose, and have good drainage capabilities.\n\n", 
        "3. Growth period:\n", 
        "It usually takes about 40 to 60 days for amaranth leaves to develop from seeds to the harvest stage.\n\n", 
        "4. Main harvesting season:\n", 
        "The ideal time for harvesting amaranth leaves is when the plants have reached a sufficient size, and the leaves are juicy and vibrant green. Amaranth leaves are typically harvested when the plants are still young, before they begin to flower.\n\n", 
    ),

    1: (
        "1. Health benefits:\n", 
        "Apples are rich in vitamin C, a powerful antioxidant that helps boost the immune system. Apples also contain anti-inflammatory and anti-cancer compounds, which may help reduce the risk of certain diseases.\n\n", 
        "2. Suitable for cultivation in:\n", 
        "Apples thrive in regions with a cool, moist climate and ample sunlight. Places with cold winters are also suitable environments for apple cultivation.\n\n", 
        "3. Growth period:\n", 
        "Typically, it takes apples 2 to 5 years to grow from the sapling stage to fruit-bearing.\n\n", 
        "4. Main harvesting season:\n", 
        "The main apple harvesting season usually occurs in late summer and early fall. The harvest time can extend from August to November.\n\n"
    ),

    2: (
        "1. Health benefits:\n", 
        "Cabbage contains high levels of vitamin C, K, and antioxidants, which help boost the immune system. It also contains anti-inflammatory and anti-cancer compounds, reducing the risk of certain serious illnesses.\n\n", 
        "2. Suitable for cultivation in:\n", 
        "Cabbage thrives best in regions with a cool and moist climate. Optimal conditions for growing cabbage include abundant sunlight and soil with stable pH levels.\n\n", 
        "3. Growth period:\n", 
        "Typically, it takes around 80 to 180 days for cabbage plants to develop from seeds to the harvest stage.\n\n", 
        "4. Main harvesting season:\n", 
        "The primary harvesting season for cabbage usually occurs in late summer and early fall. At this time, cabbage has reached its optimal size and developed a sweet taste.\n\n", 
    ),

    3: (
        "1. Health benefits:\n", 
        "Crown daisy greens are rich in vitamin A, vitamin C, fiber, and antioxidants, which help boost the immune system and maintain cardiovascular health. Crown daisy greens can also support gut health and enhance bacterial resistance.\n\n", 
        "2. Suitable for cultivation in:\n", 
        "Crown daisy greens are suitable for cultivation in various geographical regions and climates. The soil for growing crown daisy greens should be rich in organic matter, loose, and have good drainage capabilities.\n\n", 
        "3. Growth period:\n", 
        "Typically, it takes about 45 to 65 days for crown daisy greens to develop from seeds to the harvest stage.\n\n", 
        "4. Main harvesting season:\n", 
        "Crown daisy greens are usually harvested when the plants have reached a sufficient size, and the leaves are juicy and vibrant green. The roots of the plant have also formed and are suitable for harvesting.\n\n", 
    ),

    4: (
        "1. Health benefits:\n", 
        "Cucumbers are a water-rich fruit low in calories, while providing essential nutrients for good health. They are a good source of vitamin K, vitamin C, and antioxidants, which help strengthen the immune system.\n\n", 
        "2. Suitable for cultivation in:\n", 
        "Cucumbers are suitable for cultivation in warm or temperate regions. The soil for growing cucumbers should have good drainage capabilities and be rich in organic matter.\n\n", 
        "3. Growth period:\n", 
        "Typically, it takes around 50 to 70 days from seed sowing to harvest for cucumbers.\n\n", 
        "4. Main harvesting season:\n", 
        "Cucumbers are harvested when they have reached the appropriate size and exhibit signs such as bright color, smooth and crisp skin, indicating optimal ripeness.\n\n", 
    ),

    5: (
        "1. Health benefits:\n", 
        "Lettuce is a good source of vitamin K, vitamin A, vitamin C, and fiber. It helps strengthen the immune system, enhance cardiovascular health, maintain healthy skin, and support the digestion process.\n\n", 
        "2. Suitable for cultivation in:\n", 
        "Lettuce is suitable for cultivation in various geographical regions and climates. The soil for growing lettuce should have good drainage, be rich in organic matter, and be nutrient-rich.\n\n", 
        "3. Growth period:\n", 
        "Lettuce typically takes about 40 to 70 days to develop from seeds or seedlings to the stage where the leaves can be harvested.\n\n", 
        "4. Main harvesting season:\n", 
        "Lettuce is usually harvested when it has reached the desired size, and the leaves are still fresh and have a vibrant green color.\n\n", 
    ),

   6: (
        "1. Health benefits:\n", 
        "Oranges are a fruit rich in vitamin C, carotenoids, and fiber, providing numerous health benefits such as boosting the immune system, protecting the eyes, supporting digestion, and maintaining blood sugar balance.\n\n", 
        "2. Suitable for cultivation in:\n", 
        "Oranges thrive in warm and tropical climates, such as the Mediterranean region and countries in Southeast Asia. The soil should have good drainage and be nutrient-rich to support the growth and development of oranges.\n\n", 
        "3. Growth period:\n", 
        "Some varieties of oranges can take 2 to 4 years for young trees to mature and bear fruit.\n\n", 
        "4. Main harvesting season:\n", 
        "The main harvesting season for oranges typically occurs during winter and spring, varying depending on the specific kind of oranges and geographical region.\n\n", 
    ), 

    7: (
        "1. Health benefits:\n", 
        "Green onions are rich in vitamin C, vitamin B6, folate, and fiber. They have anti-inflammatory properties, boost the immune system, and support the digestion process. They may also help reduce the risk of certain diseases, such as heart disease and diabetes.\n\n", 
        "2. Suitable for cultivation in:\n", 
        "Green onions are suitable for cultivation in cool or temperate climates. They require direct sunlight, and the soil should be sandy or a suitable mixture of sand and soil.\n\n", 
        "3. Growth period:\n", 
        "Green onions can take approximately 60 to 120 days to develop from seeds or seedlings to the stage where the leaves can be harvested.\n\n", 
        "4. Main harvesting season:\n", 
        "Green onions are usually harvested when the plants have reached the desired size, and the leaves have the desired size and color. Harvesting can be done throughout the growing season, depending on the specific needs and preferences.\n\n", 
    ),

    8: (
        "1. Health benefits:\n", 
        "Tomatoes are an excellent source of vitamin C, vitamin A, antioxidants, and fiber. They provide lycopene, which helps reduce the risk of heart disease, cancer, and other illnesses.\n\n", 
        "2. Suitable for cultivation in:\n", 
        "Tomatoes are suitable for cultivation in warm and sunny climates. The soil for growing tomatoes should be rich in organic matter, well-draining, and have good water permeability.\n\n", 
        "3. Growth period:\n", 
        "However, typically, tomatoes take about 60 to 90 days to develop from planting seeds or seedlings to the stage where the fruits can be harvested.\n\n", 
        "4. Main harvesting season:\n", 
        "Tomatoes are usually harvested when the fruits have reached the desired size and color. Signs of ripeness include vibrant red color, firmness, and a gentle yield when touched.\n\n", 
    ),

    9: (
        "1. Health benefits:\n", 
        "Water spinach is a good source of vitamin A, vitamin C, antioxidants, and fiber. It provides various minerals such as iron, calcium, potassium, and magnesium, which help enhance bone and teeth strength.\n\n", 
        "2. Suitable for cultivation in:\n", 
        "Water spinach is suitable for cultivation in warm or temperate climate regions. The soil for growing water spinach should be rich in organic matter, have good drainage, and be nutrient-rich.\n\n", 
        "3. Growth period:\n", 
        "Typically, water spinach can be harvested within about 30 to 45 days after sowing seeds or transplanting seedlings.\n\n", 
        "4. Main harvesting season:\n", 
        "Water spinach is usually harvested when the plants have reached the desired size, and the leaves and stems are still fresh and have a vibrant green color.\n", 
    ),
}

CNN_map_kind = {
    0: "Herbaceous", 
    1: "Wood",
    2: "Herbaceous",
    3: "Herbaceous",
    4: "Herbaceous",
    5: "Herbaceous",
    6: "Wood",
    7: "Herbaceous",
    8: "Herbaceous",
    9: "Herbaceous",
}









