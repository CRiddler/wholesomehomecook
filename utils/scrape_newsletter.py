import requests
import bs4

text = '''
Date	Name of Newsletter	Newsletter Link	Short Text	Video Topic
3/16/2024	Veggie Spotlight: Onions	https://view.flodesk.com/emails/65e792d71caf744c3a71b378	What are the differences between red, white, and yellow onions? Can I avoid Crying?
3/23/2024	Veggie Spotlight: Kale	https://view.flodesk.com/emails/65fb0e88708082f815b464af	How do I pick the best kale? What are ways to eat kale?
3/30/2024	Veggie Spotlight: Leeks	https://view.flodesk.com/emails/6603402b62143956984827f2	Here is what to do with those fresh leeks you see at the store!
4/6/2024	Veggie Spotlight: Butternut Squash	https://view.flodesk.com/emails/660c39c71b174e5be14730a0	How to use butternut squash outside of just roasting
4/13/2024	Veggie Spotlight: Asparagus	https://view.flodesk.com/emails/6615d26abe30196ef22d9ddb	Everything you need to know about asparagus to buy and cook in your own home
4/20/2024	Veggie Spotlight: Potatoes	https://view.flodesk.com/emails/661ffa5de4ccfd05eca86779	Did you know there are starchy and waxy white potatoes? What is the difference between the two?
4/27/2024	Veggie Spotlight: Radish	https://view.flodesk.com/emails/66283a5428a7e5f04ade023f	Radishes can be so much more than a garnish!
5/4/2024	Veggie Spotlight: Cabbage	https://view.flodesk.com/emails/663276e3394170ba335a498e	Think you don't like cabbage? Read this article and try cooking a new cabbage recipe!
5/11/2024	Veggie Spotlight: Sweet Potato	https://view.flodesk.com/emails/663a568632206fb8adc505dd	What is the difference between a sweet potato and a yam?
5/18/2024	Veggie Spotlight: Carrots	https://view.flodesk.com/emails/663a56a1b5a0ac8c737bfb70	Baby carrots don't exist!
5/25/2024	Veggie Spotlight: Strawberries 	https://view.flodesk.com/emails/663a56af7464ef8193667560	Seasonality matters for flavor!
6/1/2024	Veggie Spotlight: English Peas	https://view.flodesk.com/emails/66576e768e52b589b2fe8de1	Peas are in season but did you know this about frozen pea's?
6/8/2024	Veggie Spotlight: Zuchinni	https://view.flodesk.com/emails/66609711913179a34699ec90	Did you know Zucchini can be eaten raw?	Grilled Zucchini
6/15/2024	Veggie Spotlight: Peaches	https://view.flodesk.com/emails/666885f73a0b30d63fa7a955	It is Peach Season! (June-August)	Grilled Peaches, Peach Salsa, Peach Cobbler,
6/22/2024	Veggie Spotlight: Cucumber	https://view.flodesk.com/emails/667493326fa62ef365736d46	How many varieties of cucumbers can you name?	Cherrie Garcia Smoothie
'''

template = '''
  <a href="{url}" class="text-decoration-none" target="_blank">
    <div class="card h-100" style="min-height: inherit">
      <img src="{img}" class="card-img-top" alt="..." style="min-height: 15vh">
      <div class="card-body">
        <h3 class="card-title fw-bold">{title}</h3>
        <p class="card-text">{description}</p>
      </div>
    </div>
  </a>
'''

print('<div class="d-flex flex-wrap justify-content-around">')
for line in text.strip().splitlines()[1:]:
    date, title, url, desc, *_ = line.split('\t')
    if not url:
        continue
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, features='lxml')
    img = soup.find_all('img')[1]['src']

    print(
        template.format(title=title, url=url, img=img, description=desc)
    )
print('</div>'

