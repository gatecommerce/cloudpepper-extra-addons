# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import base64
base64.encodestring = base64.encodebytes


class ProductImage(models.Model):
    _inherit = 'product.image'

    def set_image(self):
        product = self.env['product.template'].search([('name','like',self._context.get('default_name'))])
        product.image_1920 = self.image_1920
        return True

class product_template(models.Model):
    _inherit = "product.template"

    url = fields.Char('URL')
    
    def write(self, vals):
        super(product_template, self).write(vals)
        if vals.get('url'):
            img = self.process_url(vals.get('url'), self.id)
        return True

    def pre_process_url(self, raw_url):
     if ' ' not in raw_url[-1]:
        raw_url = raw_url.replace(' ', '%20')
        return raw_url
     elif ' ' in raw_url[-1]:
        raw_url = raw_url[:-1]
        raw_url = raw_url.replace(' ', '%20')
        return raw_url

    def process_url(self, url, prod_temp_id_bi):
        html_data = urllib.request.urlopen(urllib.request.Request(url,None, headers={'User-Agent': 'Mozilla/5.0'}))
        soup = BeautifulSoup(html_data,"html.parser")
        images = []
        for img in soup.findAll('img'):
            images.append(img.get('src'))
        if not images:
            imgdata = base64.encodestring(urllib.request.urlopen(urllib.request.Request(url,None, headers={'User-Agent': 'Mozilla/5.0'})).read())
            file_name = url.split('/')[-1]
            prod = self.env['product.image'].create({
                                          'product_tmpl_id':prod_temp_id_bi,
                                          'name':file_name,
                                          'image_1920':imgdata
                                          })
        for imgurl in images:
            try:
                imgurl = self.pre_process_url(imgurl)
                imgdata = base64.encodestring(urllib.request.urlopen(imgurl).read())
                file_name = imgurl.split('/')[-1]

                vals = {
                      'product_tmpl_id':prod_temp_id_bi,
                      'name':file_name,
                      'image_1920':imgdata
                      }
                record = self.env['product.image'].create(vals)
            except:
                pass

    @api.model_create_multi
    def create(self, vals_list):
        res = super(product_template, self).create(vals_list)
        if res.url:
            img = self.process_url(vals.get('url'), res.id)
        return res
