#!/usr/bin/env python
import lanplunger

lanplunger.app.config.from_object('config.DebugConfiguration')


lanplunger.app.run(host='0.0.0.0', port=8000, debug=True)
