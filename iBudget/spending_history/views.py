"""
This module provides functions for handling spending_history view.
"""

import json
from datetime import date, timedelta
from decimal import Decimal

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from group.models import SharedSpendingCategories, Group, UsersInGroups, SharedFunds
from utils.get_role import groups_for_user, is_user_member_group, is_user_admin_group
from utils.spendings_limit_checker import compare_ind_spend_limit
from utils.validators import input_spending_registration_validate, is_valid_data_spending_history, \
    date_parse
from .models import SpendingCategories, SpendingHistory, FundCategories


@require_http_methods(["POST"])
def register_spending(request):
    """Handling request for creating of spending categories list.
        Args:
            request (HttpRequest): request from server which contain
            fund, category, sum, date, comment
        Returns:
            HttpResponse status.
    """
    data = json.loads(request.body)
    if not input_spending_registration_validate(data):
        return HttpResponse(status=400)

    user = request.user
    spending = SpendingCategories.get_by_id(int(data["category"]))
    fund = FundCategories.get_by_id(int(data["type_of_pay"]))
    if not spending and not fund:
        return HttpResponse(status=400)
    if spending.is_shared:
        if not SharedSpendingCategories.get_by_spending_id(spending.id):
            return HttpResponse(status=403)
    else:
        if not spending.owner == user:
            return HttpResponse(status=403)

    value = Decimal(data["value"])
    comment = data["comment"]

    spending_history = SpendingHistory(
        fund=fund,
        spending_categories=spending,
        date=data["date"],
        value=value,
        owner=user,
        comment=comment
    )
    try:
        spending_history.save()
    except(ValueError, AttributeError):
        return HttpResponse(status=406)
    response = f"You've just register spending {spending.name}. \n" +\
               compare_ind_spend_limit(user, data["date"], spending, value)
    return HttpResponse(response, status=201)


def create_spending_history_individual(user, start_date, finish_date, utc_difference):
    """Creating array of data for individual spending history.
        Args:
            user (UserProfile): user.
            start_date (date): The beginning of statistic period
            finish_date (date): The end of statistic period
            utc_difference(int): difference between user's time and UTC
        Returns:
            Array of data for individual spending history statistic.
    """

    history_individual = []
    for entry in SpendingCategories.filter_by_user(user):
        history_individual_entry = []
        for item in SpendingHistory.filter_by_user_date_spending(user,
                                                                 start_date,
                                                                 finish_date,
                                                                 entry):
            history_individual_entry.append({'value': float(item.value),
                                             'date': (item.date +
                                                      timedelta(hours=utc_difference)).date(),
                                             'fund': item.fund.name,
                                             'spending_history_id':item.id})
        if history_individual_entry:
            history_individual.append({'spending': entry.name,
                                       'history': history_individual_entry})
    for group in groups_for_user(user):
        if is_user_member_group(group, user):
            for entry in SharedSpendingCategories.filter_by_group(group=group):
                history_individual_entry = []
                for item in SpendingHistory.filter_by_user_date_spending(user,
                                                                         start_date,
                                                                         finish_date,
                                                                         spending_categories=entry):
                    history_individual_entry.append({'value': float(item.value),
                                                     'date': (item.date +
                                                              timedelta(hours
                                                                        =utc_difference)).date(),
                                                     'fund': item.fund.name,
                                                     'spending_history_id': item.id})
                if history_individual_entry:
                    history_individual.append({'spending': entry.name
                                                           + ' / '
                                                           + Group.get_group_by_id(group).name,
                                               'history': history_individual_entry})

    return history_individual


def create_spending_history_for_admin(user, start_date, finish_date, utc_difference):
    """Creating array of spending history data for admin.
        Args:
            user (UserProfile): user who needs information.
            start_date (date): The beginning of statistic period
            finish_date (date): The end of statistic period
        Returns:
            Array of spending history data for admin.
    """
    history_for_admin = []
    groups_for_admin = [group for group in groups_for_user(user)
                        if is_user_admin_group(group, user)]

    for group in groups_for_admin:

        for entry in SharedSpendingCategories.filter_by_group(group=group):

            history_spending_category = []

            for person in UsersInGroups.filter_by_group(group=group):
                history_person = []
                if is_user_member_group(group, person):
                    for item in SpendingHistory.filter_by_user_date_spending(person,
                                                                             start_date,
                                                                             finish_date,
                                                                             entry):
                        history_person.append({'member': person.email,
                                               'value': float(item.value),
                                               'date': (item.date +
                                                        timedelta(hours=utc_difference)).date(),
                                               'fund': 'Individual fund',
                                               'spending_history_id': item.id})
                else:
                    for item in SpendingHistory.filter_by_user_date_spending(person,
                                                                             start_date,
                                                                             finish_date,
                                                                             entry):
                        fund_entry = item.fund.name \
                            if item.fund in SharedFunds.filter_by_group(group=group) \
                            else 'Individual fund'
                        history_person.append({'member': person.email,
                                               'value': float(item.value),
                                               'date': (item.date +
                                                        timedelta(hours=utc_difference)).date(),
                                               'fund': fund_entry,
                                               'spending_history_id': item.id})

                if history_person:
                    history_spending_category.extend(history_person)

            if history_spending_category:
                history_for_admin.append({'spending': entry.name
                                                      + ' / '
                                                      + Group.get_group_by_id(group).name,
                                          'history': history_spending_category})
    return history_for_admin


@require_http_methods(["POST"])
def create_spending_history(request):
    """Handling request for creating spending history data.

        Args:
            request (HttpRequest): contains start date, final date and UTC information.
        Returns:
            JsonResponse object.
    """
    user = request.user
    data = json.loads(request.body)
    if not is_valid_data_spending_history(data):
        return HttpResponse(status=400)

    start_date, finish_date = date_parse(data)
    utc_difference = int(data['UTC'])
    if start_date > finish_date:
        return JsonResponse({}, status=400)

    if user:
        return JsonResponse({'individual':
                                 create_spending_history_individual(user,
                                                                    start_date,
                                                                    finish_date,
                                                                    utc_difference),
                             'admin':
                                 create_spending_history_for_admin(user,
                                                                   start_date,
                                                                   finish_date,
                                                                   utc_difference)},
                            status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["GET"])
def get_month_spending(request):
    """Handling request for representation total sum.
        Args:
            request (HttpRequest): data.
        Returns:
            HttpResponse object.
    """
    user = request.user
    finish_date = date.today()
    start_date = date(finish_date.year, finish_date.month, 1)

    if user:
        return HttpResponse(SpendingHistory.filter_by_user_date_spending(user,
                                                                         start_date,
                                                                         finish_date),
                            status=200)
    return HttpResponse('Bad Request', status=400)

def create_spending_chart(user, start_date, finish_date):
    """Creating array of data for spending history chart.
        Args:
            user (UserProfile): user.
            start_date (date): The beginning of statistic period
            finish_date (date): The end of statistic period
        Returns:
            Array of data for individual spending history statistic.
    """
    list_spending_value = list()
    list_spending_name = list()
    list_spending_id = list(set(SpendingHistory.filter_by_user_date(
        user,
        start_date,
        finish_date).values_list('spending_categories_id', flat=True)))
    for item in list_spending_id:
        list_spending_name.append(SpendingCategories.get_by_id(item).name)
        total = sum(SpendingHistory.filter_by_user_date_spending(
            user,
            start_date,
            finish_date,
            SpendingCategories.get_by_id(item)).values_list('value', flat=True))
        list_spending_value.append(total)
    return {'value': list_spending_value, 'name': list_spending_name}

@require_http_methods(["POST"])
def get_spending_chart(request):
    """Handling request for creating spending history data.

        Args:
            request (HttpRequest): contains start date, final date and UTC information.
        Returns:
            JsonResponse object.
    """
    user = request.user
    data = json.loads(request.body)
    if not is_valid_data_spending_history(data):
        return HttpResponse(status=400)
    start_date, finish_date = date_parse(data)

    if start_date > finish_date:
        return JsonResponse({}, status=400)

    if user:
        return JsonResponse(create_spending_chart(user, start_date, finish_date),
                            status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["DELETE"])
def delete_spending_history(request, spending_history_id):
    """Handling request for delete group.
        Args:
            request (HttpRequest): Data for delete spending history category.
            spending_history_id: Spending history id
        Returns:
            HttpResponse object.
    """
    user = request.user
    spending_history = SpendingHistory.get_by_id(spending_history_id)
    if not spending_history:
        return HttpResponse(status=406)
    if not spending_history.owner == user:
        return HttpResponse(status=400)
    spending_history.update(is_active=False)
    return HttpResponse("You've just deleted this spending from your history", status=200)

