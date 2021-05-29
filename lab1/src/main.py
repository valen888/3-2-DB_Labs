from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lxml import etree
import os
import webbrowser


def cleanup():
    try:
        os.remove("../results/ukr_net.xml")
        os.remove("../results/repka.xml")
        os.remove("../results/repka.xhtml")
    except OSError:
        pass


def scrap_data():
    process = CrawlerProcess(get_project_settings())
    process.crawl('ukr_net')
    process.crawl('repka')
    process.start()


def task2():
    print("Середня кількість текстових фрагментів для сайту ukr.net")
    root = etree.parse("../results/ukr_net.xml")
    pages = root.xpath("//page")
    count = 0
    sum_of_fragments = 0
    for page in pages:
        count = count + 1
        sum_of_fragments = sum_of_fragments + page.xpath("count(fragment[@type='text'])")
    print("Середнє значення: %d" % (sum_of_fragments/count))


def task3_4():
    print("Товари з REPKA")
    transform = etree.XSLT(etree.parse("repka.xsl"))
    result = etree.parse("../results/repka.xml")
    result.write("../results/repka.xhtml", pretty_print=True, encoding="UTF-8")
    webbrowser.open('file://' + os.path.realpath("../results/repka.xhtml"))


if __name__ == '__main__':
    cleanup()
    scrap_data()
        print("*" * 50)
    while True:
        print("1. Завдання 2")
        print("2. Завдання 3-4")
        print("> ", end='', flush=True)
        number = input()
        if number == "1":
            task2()
        elif number == "2":
            task3_4()
        else:
            break
