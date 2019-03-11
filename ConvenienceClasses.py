import numpy as np
import ipywidgets as widgets

from scipy.interpolate import CubicSpline
from scipy.ndimage.filters import gaussian_filter1d


# --------------------- Classes -------------------------
# Convenience Class for Plot Handles
class SingleLinePlotHandle:
    def __init__(self, ax, l):
        self.ax = ax
        self.l = l
        
# Custom Class for Interpolating Splines     
class Interpolated(object):
    def __init__(self, x, y, sigma):
        self.x = x
        self.y = y
        self.sigma = sigma
        self.handles = []
    
    def override(self, x, y, sigma):
        self.x = x
        self.y = y
        self.sigma = sigma
    
    def getHighCurv(self, threshold):
        # points of max / min curvature, thresholded based on magnitude of curvature
        roots = self._curv_roots[~np.isnan(self._curv_roots)] # remove nans -- TODO address root problem (!)
        return roots[(np.abs(self._curv(roots)) > threshold)]
        # return self._curv_roots[(np.abs(self._curv(self._curv_roots)) > threshold)]
    
    def getInflectionPoints(self, threshold):
        # points of zero curvature, thresholded based on magnitude of gradient
        roots = self._grad_roots[~np.isnan(self._grad_roots)] # remove nans -- TODO address root problem (!)
        return roots[(np.abs(self._grad(roots)) > threshold)]
        # return self._grad_roots[(np.abs(self._grad(self._grad_roots)) > threshold)]
    
    @property
    def spline(self):
        return self._spline
    
    @property
    def grad(self):
        return self._grad
    
    @property
    def curv(self):
        return self._curv
    
    @property
    def sigma(self):
        return self._sigma
    
    @sigma.setter
    def sigma(self, s):
        self._sigma = s
        if (self._sigma == 0):
            self._spline = CubicSpline(self.x, self.y, bc_type='not-a-knot')
        else:
            self._spline = CubicSpline(self.x, gaussian_filter1d(self.y, self._sigma), bc_type='not-a-knot')
        self._grad = self._spline.derivative(1)
        self._curv = self._spline.derivative(2)
        self._curv_roots = self._spline.derivative(3).roots(discontinuity=True)
        self._grad_roots = self._curv.roots(discontinuity=True)

# Custom Class for Controls     
class ParamControl():
    def __init__(self, param, ax_param, ax_grad, ax_curv, label=None):
        self._param = param
        self._ax_param = ax_param
        self._ax_grad = ax_grad
        self._ax_curv = ax_curv
        self._hc_color = '#0E6089'
        self._if_color = '#5E50A3'
        # ------ thresholds ------
        self.sigma_control = widgets.FloatSlider(orientation='horizontal', description='$\sigma$', value=self._param.sigma, min=0, max=5, continuous_update=True)
        # ------ thresholds ------
        self.curvature_threshold = widgets.FloatSlider(orientation='horizontal', description='$\\nabla^2$', value=30000, min=0, max=max(self._param.handles[2].l.get_ydata())*1.05, continuous_update=True)
        self.gradient_threshold = widgets.FloatSlider(orientation='horizontal', description='$\\nabla$', value=130, min=0, max=max(self._param.handles[1].l.get_ydata())*1.05, continuous_update=True)
        self._c_handle = self._ax_curv.axhline(y=self.curvature_threshold.value, color='black', linestyle=':', alpha=0.7)
        self._g_handle = self._ax_grad.axhline(y=self.gradient_threshold.value, color='black', linestyle=':', alpha=0.7)
        self.label = label
        # ------ points of high curvature ------
        roots = self._param.getHighCurv(self.curvature_threshold.value)
        self._hc_handles = []
        for i in range(len(roots)):
            l = self._ax_param.axvline(x=roots[i], color=self._hc_color, linestyle='--', alpha=0.4)
            self._hc_handles.append(l)
        # ------ inflection points ------
        roots = self._param.getInflectionPoints(self.gradient_threshold.value)
        self._if_handles = []
        for i in range(len(roots)):
            l = self._ax_param.axvline(x=roots[i], color=self._if_color, linestyle=':', alpha=0.4)
            self._if_handles.append(l)
    
    @property
    def label(self):
        return self._label
    
    @label.setter
    def label(self, l):
        self._label = l
        if (self._label is None):
            self.widget = widgets.VBox([self.sigma_control, self.gradient_threshold, self.curvature_threshold])
        else:
            self.widget = widgets.VBox([widgets.Label(value=self._label), self.sigma_control, self.gradient_threshold, self.curvature_threshold])
    
    def setColors(self, hc_color, if_color):
        self._hc_color = hc_color
        self._if_color = if_color
        for i in range(len(self._hc_handles)):
            self._hc_handles[i].set_color(self._hc_color) 
        for i in range(len(self._if_handles)):
            self._if_handles[i].set_color(self._if_color) 
    
    def update_curv(self):
        self._c_handle.set_ydata(self.curvature_threshold.value)    
        # ------ update roots ------
        new_roots = self._param.getHighCurv(self.curvature_threshold.value)
        nNew = len(new_roots)
        nOld = len(self._hc_handles)
        nUpdate = min(nNew, nOld)
        for i in range(nUpdate): # update
            l = self._hc_handles[i]
            l.set_xdata(new_roots[i])
            l.set_visible(True)
        for i in range(max(nNew-nOld, 0)): # add
            l = self._ax_param.axvline(x=new_roots[i+nUpdate], color=self._hc_color, linestyle='--', alpha=0.4)
            l.set_visible(True)
            self._hc_handles.append(l)
        for i in range(max(nOld - nNew, 0)): # hide
            self._hc_handles[i+nUpdate].set_visible(False)
    
    def update_grad(self):
        self._g_handle.set_ydata(self.gradient_threshold.value)
        # ------ update roots ------
        new_roots = self._param.getInflectionPoints(self.gradient_threshold.value)
        nNew = len(new_roots)
        nOld = len(self._if_handles)
        nUpdate = min(nNew, nOld)
        for i in range(nUpdate): # update
            l = self._if_handles[i]
            l.set_xdata(new_roots[i])
            l.set_visible(True)
        for i in range(max(nNew-nOld, 0)): # add
            l = self._ax_param.axvline(x=new_roots[i+nUpdate], color=self._if_color, linestyle=':', alpha=0.4)
            l.set_visible(True)
            self._if_handles.append(l)
        for i in range(max(nOld - nNew, 0)): # hide
            self._if_handles[i+nUpdate].set_visible(False)
    
    def _update_param(self, xs):
        self._param.sigma = self.sigma_control.value
        self._param.handles[0].l.set_ydata(self._param.spline(xs))
        
        ydata = np.abs(self._param.grad(xs))
        self._param.handles[1].l.set_ydata(ydata)
        self.gradient_threshold.max = max(ydata*1.05)
        self._param.handles[1].ax.relim()
        self._param.handles[1].ax.autoscale(axis='y')
        
        ydata = np.abs(self._param.curv(xs))
        self._param.handles[2].l.set_ydata(ydata)
        self.curvature_threshold.max = max(ydata*1.05)
        self._param.handles[2].ax.relim()
        self._param.handles[2].ax.autoscale(axis='y')
    
    def update_full(self, xs):
        self._update_param(xs)
        self.update_curv()
        self.update_grad()

# Wrapper for Quick Object
class QuickObj:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

