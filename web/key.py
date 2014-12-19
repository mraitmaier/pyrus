#
#
import base64

def _generate_key():
    '''Generate a unique session ID for a particular user.'''
    base = base64.b64encode(bytearray('This#is%quite!long:string,?OK*for&now.', 'utf-8'))
    # we need to replace some chars, they cannot be used in filename;
    # currently the problem is only '/'
    return base.replace(b'/', b'$')

