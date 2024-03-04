from lxml import etree
import re
import openpyxl

workbook = openpyxl.Workbook()

worksheet = workbook.active

worksheet['A1'] = '漏洞名称'
worksheet['B1'] = '漏洞详情'
worksheet['C1'] = '修复建议'

content = open('index.html', encoding='utf8').read()

selector = etree.HTML(content)

high_size_xpath = '//*[@id="content"]/div[8]/div[2]/div/text()[2]'

middle_size_xpath = '//*[@id="content"]/div[8]/div[2]/div/text()[3]'

high_size = selector.xpath(high_size_xpath)[0]

high_size = int(high_size.strip().replace("高风险", "").replace("[", "").replace("]", ""))

middle_size = selector.xpath(middle_size_xpath)[0]

middle_size = int(middle_size.strip().replace("中危险", "").replace("[", "").replace("]", ""))

vuln_size = middle_size + high_size

for i in range(1, vuln_size + 1):

    j = i + 1

    i = i * 2 - 1

    vuln_title_xpath = '//*[@id="vuln_distribution"]/tbody/tr[' + str(i) + ']/td[2]/span/text()'

    title = selector.xpath(vuln_title_xpath)

    print(j, ": " ,title[0].strip())

    worksheet['A' + str(j)] = title[0].strip()

print("漏洞描述")

for i in range(1, vuln_size + 1):

    j = i + 1

    i = i * 2

    xpath = '/html/body/div/div[4]/div[8]/div[2]/table/tbody/tr[' + str(i) + ']/td/table/tr[2]/td/text()'

    title = selector.xpath(xpath)

    # print(i, ": " ,matches[0])

    print(j)

    worksheet['B' + str(j)] = title[0]

print("修复建议")

for i in range(1, vuln_size + 1):

    j = i + 1

    i = i * 2

    xpath = '/html/body/div/div[4]/div[8]/div[2]/table/tbody/tr[' + str(i) + ']/td/table/tr[3]/td/text()'

    title = selector.xpath(xpath)

    # print(i, ": " ,matches[0])

    print(j)

    worksheet['C' + str(j)] = title[0]

workbook.save('output.xlsx')

workbook.close()
