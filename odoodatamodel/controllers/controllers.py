# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from odoo.tools import date_utils
import requests


class Odoodatamodel(http.Controller):


    @http.route(['/data-model'], auth='user')
    def er_diagram(self, **kw):
        return request.render('odoodatamodel.er_template')

    @http.route('/relationfinder/', type='http', auth='public', methods=['GET', 'OPTIONS'], csrf=False, cors='*')
    def index(self, **kw):
        request.cr.execute(
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME ASC;")
        tableList = list(request.cr.fetchall())
        y = dict()
        errorList = []
        colNum = dict()
        recNum = dict()
        yy = dict()

        for table in tableList:
            tableName = str(table[0]).replace("_", ".")
            # print(tableName)

            try:
                x = dict(request.env[tableName].sudo().fields_get())
                # FOR COL
                total_len = request.env[tableName].sudo().search_count([])

                colNum[table[0]] = len(x)
                recNum[table[0]] = total_len

                y[table[0]] = x
            except:
                errorList.append(tableName)
        result = {"tables": y, "errorTables": errorList, "rows": recNum, "total records": len(y)}

        result = json.dumps(result)

        return str(result)

    @http.route('/relations/', auth='public')
    def relats(self, **kw):
        mainKey = "relation"
        request.cr.execute(
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME ASC;")
        tableList = list(request.cr.fetchall())
        y = dict()
        errorList = []
        for table in tableList:
            tableName = str(table[0]).replace("_", ".")
            try:
                x = dict(request.env[tableName].sudo().fields_get())
                relList = dict()
                for vers in x.keys():
                    if "relation" in x[vers].keys():
                        relList[vers] = x[vers]
                y[table[0]] = relList
            except:
                pass

        result = {"tables": y}
        result = json.dumps(result)
        tables = str(result)  # skip this later
        return tables

    @http.route('/relationtable/', auth='public')
    def relattable(self, **kw):
        request.cr.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'user_notify_rel';")
        data = list(request.cr.fetchall())
        # request.cr.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'docket.notifii';")
        # data = list(request.cr.fetchall())
        return str(data)

    @http.route('/relation/search/<string:var>/', type='http', auth='public', methods=['GET', 'OPTIONS'], csrf=False,
                cors='*')
    def search(self, var, **kw):

        request.cr.execute(
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME ASC;")
        tableList = list(request.cr.fetchall())
        y = dict()
        errorList = []
        for table in tableList:
            tableName = str(table[0]).replace("_", ".")
            try:
                x = dict(request.env[tableName].sudo().fields_get())
                y[table[0]] = x
            except:
                errorList.append(tableName)
        result = {"tables": y, "errorTables": errorList}
        result = json.dumps(result)

        final = []

        for table in y.keys():
            for column in y[table].keys():
                if var == column:
                    final.append(table)
                    break

        return str(json.dumps({"result": final}))

    # MINI TABLUEA

    @http.route('/report/<int:id>', type='http', auth="user", website=True, csrf=False)
    def show_saved_report(self, **kw):
        report_id = kw.get('id')
        reports = request.env['mini.tableau'].sudo().search([('id', '=', report_id)])

        request.cr.execute(reports.user_query)
        table_column_names = request.cr.description
        table_column_names = [
            column_name[0] for column_name in table_column_names
        ]

        table_result = request.cr.fetchall()

        data = {

            'sql_query': reports.user_query,
            'user_query': reports.user_query,
            'report_name': reports.report_name or '',
            'report_rows': reports.report_rows or '',
            'report_columns': reports.report_columns or '',
            'chart_type': reports.chart_type or ''
        }

        return request.render('mini_tableau.saved_report_dashboard_template', data)

    @http.route('/save-report/', type='http', auth="user", website=True, csrf=False)
    def save_report(self, **kw):
        report_object = request.env['mini.tableau'].sudo()
        report_name = kw.get('report_name')
        sql_query = kw.get('sql_query')

        report_object.create({
            "user_query": sql_query,
            'report_name': report_name,
        })

        # self.chart_type = chart_type
        return request.redirect('/query-dashboard')

    @http.route('/query-dashboard', type='http', auth="user", website=True, csrf=False)
    def query_dashboard(self, **kw):
        request.cr.execute(
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_NAME ASC;")

        tables = request.cr.fetchall()
        reports = request.env['mini.tableau'].sudo().search([])

        data = {
            'tables': tables,
            'reports': reports
        }

        return request.render('odoodatamodel.dashboard_template', data)

    @http.route('/table-result', type='json', auth='user', methods=['POST'], website=True)
    def table_result(self, **kw):
        table_name = kw.get('table_name')
        total_rows = kw.get('total_rows')
        sql_query = kw.get('sql_query')

        request.cr.execute(f'SELECT * FROM {table_name} LIMIT {total_rows};')

        table_column_names = request.cr.description
        table_column_names = [
            column_name[0] for column_name in table_column_names
        ]

        table_result = request.cr.fetchall()

        data = {
            'table_name': table_name,
            'table_column_names': table_column_names,
            'table_result': table_result
        }

        return data

    @http.route('/query-result', type='json', auth='user', methods=['POST'], website=True)
    def query_result(self, **kw):

        sql_query = kw.get('sql_query')
        message = None

        try:
            request.cr.execute(sql_query)

            table_column_names = request.cr.description
            table_column_names = [
                column_name[0] for column_name in table_column_names
            ]

            table_result = request.cr.fetchall()

            data = {
                'table_name': 'Custom query executed',
                'table_column_names': table_column_names,
                'table_result': table_result
            }

            return data

        except Exception as e:
            request.cr.rollback()
            return {'message': f'ERROR: {e}'}

    # Report Controllers
    @http.route('/report-dashboard', methods=['GET', 'POST'], type='http', auth="user", website=True, csrf=False)
    def report_dashboard(self, **kw):

        sql_query = kw.get('sql_query')
        message = None

        # sending data to the template
        request.cr.execute(sql_query)

        table_column_names = request.cr.description
        table_column_names = [
            column_name[0] for column_name in table_column_names
        ]

        data = {
            'table_column_names': sorted(table_column_names),
            'sql_query': sql_query,
        }

        return request.render('odoodatamodel.report_dashboard_template', data)

    @http.route('/query-report-result', type='json', auth='user', methods=['POST'], website=True)
    def query_result_dict(self, **kw):

        sql_query = kw.get('sql_query')
        message = None

        try:
            request.cr.execute(sql_query)

            column_names = request.cr.description
            column_names = [column_name[0] for column_name in column_names]

            rows = request.cr.fetchall()

            result_dict = {}

            for column_name in column_names:
                result_dict[column_name] = []

            for row in rows:
                for key, value in zip(column_names, row):
                    result_dict[key].append(value)

            return {'result_data': result_dict}

        except Exception as e:
            request.cr.rollback()
            return {'message': f'ERROR: {e}'}


class MiniTableauQueryController(http.Controller):
    @http.route('/save_query', type='http', auth='user', csrf=False)
    def save_query(self, query_name, query_val):
        MiniTableauQueries = request.env['mini.tableau.query']
        # print(MiniTableauQueries)
        # Create a new record with the given query name and value
        new_query = MiniTableauQueries.create({
            'query_name': query_name,
            'query_val': query_val,
            # 'query_id':query_id
        })
        print(new_query)
        print(new_query.query_name)
        return json.dumps({'success': True, 'message': 'Query saved successfully!'})

    @http.route('/delete-report/<int:query_id>', type='http', auth='user', csrf=False)
    def delete_query(self, query_id):
        query_id = int(query_id)
        MiniTableauQueries = request.env['mini.tableau.query']
        query = MiniTableauQueries.browse(query_id)
        print("done")

        # Check if the query exists
        if query:
            # Delete the query record
            print("unlink")
            query.unlink()
            return json.dumps({'success': True, 'message': 'Query deleted successfully!'})
        else:
            # Handle the case where the query does not exist
            return request.not_found()


