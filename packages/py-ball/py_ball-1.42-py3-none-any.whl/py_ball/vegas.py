#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 16:04:03 2019

@author: patrickmcfarlane

vegas.py contains the Vegas class that
enables SDQL queries of `sportsdatabase.com <https://sportsdatabase.com>`_
"""

from requests import get

SDQL_URL = "https://sportsdatabase.com/{league}/" + \
    "query.html?sdql=date%2C+line%2C+points%2C+season%2C+site%2C+team%2C+total+%40+site%3Dhome+and+date%3D{date}&submit=++S+D+Q+L+%21++"


def parse_sdql(html_text):
    """ parse_sdql extracts the data tables from the HTML
    text provided

    @param html_text (str): String of the site HTML containing
        the data table

    Returns:

        data_dict (dict): Dictionary containing SDQL data. Returns an empty
            dictionary 
    """


    start_val = html_text.find('<thead>')
    if start_val != -1:
        html_text = html_text[start_val + 7:]

        # Get column names and initialize data_dict
        column_headers = []
        data_dict = {}
        for _ in range(7):
            start_ind = html_text.find('<th>')
            end_ind = html_text.find('</th>')
            val = html_text[start_ind + 4: end_ind]
            column_headers.append(val)
            data_dict[val] = []
            html_text = html_text[end_ind + 5: ]

        # Fill in the dictionary with each row of data
        end_val = html_text.find('</tbody>')
        count = 0
        while end_val > 100:
            for columns in column_headers:
                start_ind = html_text.find('<td>')
                end_ind = html_text.find('</td>')
                val = html_text[start_ind + 4: end_ind]
                if '<b>' in val:
                    val = val.replace('<b>', '')
                    val = val.replace('</b>', '')
                data_dict[columns] = data_dict[columns] + [val]
                html_text = html_text[end_ind + 4: ]
                end_val = html_text.find('</tbody>')
            count += 1
            if count > 20:
                break

    else:
        data_dict = {}
        
    return data_dict


class Vegas:
    """ The Vegas class contains all resources needed to use query 
    `sportsdatabase.com <https://sportsdatabase.com>`_.

    The Vegas class has the following required parameters:

        @param **date** (*str*): String of a date in YYYYMMDD format.

        @param **league** (*str*): One of 'nba' or 'wnba' corresponding to
            the league of interest

    Attributes:

        **api_resp** (*dict*): Text of the HTML response from the site.

        **data** (*dict*): A dictionary of data on the provided date
            keyed by column names.
    """

    def __init__(self, headers, date, league):

        url = SDQL_URL.format(league=league,
                              date=date)

        api_response = get(url, headers=headers)
        self.api_resp = api_response.text
        # Storing the API response in a dictionary called data
        # The results can come in different formats, namely a
        # dictionary keyed by either resultSets or resultSet
        self.data = parse_sdql(self.api_resp)
