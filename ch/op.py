import logging

import cherrypy
from cryptojwt import as_bytes
from oidcmsg.oauth2 import AuthorizationRequest
from oidcmsg.oauth2 import ErrorResponse
from oidcendpoint.sdb import AuthnEvent

logger = logging.getLogger(__name__)


class OpenIDProvider(object):
    def __init__(self, config, srv_info):
        self.config = config
        self.srv_info = srv_info

    def do_response(self, endpoint, req_args, **args):
        info = endpoint.do_response(self.srv_info, request=req_args, **args)

        for key, value in info['http_headers']:
            cherrypy.response.headers[key] = value

        try:
            _response_placement = info['response_placement']
        except KeyError:
            _response_placement = endpoint.response_placement

        if _response_placement == 'body':
            logger.info('Response: {}'.format(info['response']))
            return as_bytes(info['response'])
        elif _response_placement == 'url':
            logger.info('Redirect to: {}'.format(info['response']))
            raise cherrypy.HTTPRedirect(info['response'])

    @cherrypy.expose
    def service_endpoint(self, name, **kwargs):
        logger.info(kwargs)
        logger.info('At the {} endpoint'.format(name))

        endpoint = self.srv_info.endpoint[name]

        try:
            authn = cherrypy.request.headers['Authorization']
        except KeyError:
            pr_args = {}
        else:
            pr_args = {'auth': authn}

        if endpoint.request_placement == 'body':
            if cherrypy.request.process_request_body is True:
                _request = cherrypy.request.body.read()
            else:
                raise cherrypy.HTTPError(400, 'Missing HTTP body')
            if not _request:
                _request = kwargs

            req_args = endpoint.parse_request(self.srv_info, request=_request,
                                              **pr_args)
        else:
            req_args = endpoint.parse_request(self.srv_info, request=kwargs,
                                              **pr_args)
        logger.info('request: {}'.format(req_args))

        if isinstance(req_args, ErrorResponse):
            return as_bytes(req_args.to_json())

        args = endpoint.process_request(self.srv_info, req_args)
        return self.do_response(endpoint, req_args, **args)

    @cherrypy.expose
    def authn_verify(self, url_endpoint, **kwargs):
        """
        Authentication verification

        :param authn_method: Which authn method that was used
        :param kwargs: response arguments
        :return: HTTP redirect
        """
        authn_method = self.srv_info.endpoint_to_authn_method[url_endpoint]


        username = authn_method.verify(**kwargs)
        if not username:
            cherrypy.HTTPError(403, message='Authentication failed')

        auth_args = authn_method.unpack_token(kwargs['token'])
        request = AuthorizationRequest().from_urlencoded(auth_args['query'])

        # uid, salt, valid=3600, authn_info=None, time_stamp=0, authn_time=None,
        # valid_until=None
        authn_event = AuthnEvent(username, 'salt',
                                 authn_info=auth_args['authn_class_ref'],
                                 authn_time=auth_args['iat'])

        endpoint = self.srv_info.endpoint['authorization']
        args = endpoint.post_authentication(self.srv_info, request,
                                            user=username,
                                            authn_event=authn_event)

        return self.do_response(endpoint, request, **args)

    def _cp_dispatch(self, vpath):
        # Only get here if vpath != None
        ent = cherrypy.request.remote.ip
        logger.info('ent:{}, vpath: {}'.format(ent, vpath))

        if len(vpath) == 2 and vpath[0] == 'verify':
            a = vpath.pop(0)
            b = vpath.pop(0)
            cherrypy.request.params['url_endpoint'] = '/'.join(['', a, b])
            return self.authn_verify

        for name, instance in self.srv_info.endpoint.items():
            if vpath == instance.vpath:
                cherrypy.request.params['name'] = name
                for n in range(len(vpath)):
                    vpath.pop()
                return self.service_endpoint

        return self
