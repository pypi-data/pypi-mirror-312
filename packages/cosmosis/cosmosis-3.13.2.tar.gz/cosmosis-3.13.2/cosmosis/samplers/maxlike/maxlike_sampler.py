from .. import Sampler
from ...runtime import logs
import numpy as np


class MaxlikeSampler(Sampler):
    sampler_outputs = [("prior", float), ("like", float), ("post", float)]

    def config(self):
        self.tolerance = self.read_ini("tolerance", float, 1e-3)
        self.maxiter = self.read_ini("maxiter", int, 1000)
        self.output_ini = self.read_ini("output_ini", str, "")
        self.output_cov = self.read_ini("output_covmat", str, "")
        self.method = self.read_ini("method",str,"Nelder-Mead")
        self.max_posterior = self.read_ini("max_posterior", bool, False)

        if self.max_posterior:
            logs.overview("------------------------------------------------")
            logs.overview("NOTE: Running optimizer in **max-posterior** mode:")
            logs.overview("NOTE: Will maximize the combined likelihood and prior")
            logs.overview("------------------------------------------------")
        else:
            logs.overview("--------------------------------------------------")
            logs.overview("NOTE: Running optimizer in **max-like** mode:")
            logs.overview("NOTE: not including the prior, just the likelihood.")
            logs.overview("NOTE: Set the parameter max_posterior=T to change this.")
            logs.overview("NOTE: This won't matter unless you set some non-flat")
            logs.overview("NOTE: priors in a separate priors file.")
            logs.overview("--------------------------------------------------")

        self.converged = False

    def execute(self):
        import scipy.optimize

        def likefn(p_in):
            #Check the normalization
            if (not np.all(p_in>=0)) or (not np.all(p_in<=1)):
                return np.inf
            p = self.pipeline.denormalize_vector(p_in)
            r = self.pipeline.run_results(p)
            if self.max_posterior:
                return -r.post
            else:
                return -r.like
            return -like

        # starting position in the normalized space.  This will be taken from
        # a previous sampler if available, or the values file if not.
        start_vector = self.pipeline.normalize_vector(self.start_estimate())
        bounds = [(0.0, 1.0) for p in self.pipeline.varied_params]

        # check that the starting position is a valid point
        start_like = likefn(start_vector)
        if not np.isfinite(start_like):
            raise RuntimeError('invalid starting point for maxlike')

        if self.method.lower() == "bobyqa":
            # use the specific pybobyqa minimizer
            import pybobyqa

            # this works with bounds in the form of a tuple of two arrays
            lower = np.array([b[0] for b in bounds])
            upper = np.array([b[1] for b in bounds])
            kw = {
                "seek_global_minimum": True,
                "bounds": (lower,upper),
                "print_progress": logs.is_enabled_for(logs.NOISY),
                "rhobeg": 0.1,
                "rhoend": self.tolerance,
            }
            result = pybobyqa.solve(likefn, start_vector, **kw)
            opt_norm = result.x
        else:
            # Use scipy mainimizer instead
            result = scipy.optimize.minimize(likefn, start_vector, method=self.method,
            jac=False, tol=self.tolerance,
            options={'maxiter':self.maxiter, 'disp':True})

            opt_norm = result.x

        opt = self.pipeline.denormalize_vector(opt_norm)
        
        #Some output - first log the parameters to the screen.
        results = self.pipeline.run_results(opt)
        if self.max_posterior:
            logs.overview("Best fit (by posterior):\n%s"%'   '.join(str(x) for x in opt))
        else:
            logs.overview("Best fit (by likelihood):\n%s"%'   '.join(str(x) for x in opt))
        logs.overview("Posterior: {}\n".format(results.post))
        logs.overview("Likelihood: {}\n".format(results.like))

        #Next save them to the proper table file
        self.output.parameters(opt, results.extra, results.prior, results.like, results.post)

        #If requested, create a new ini file for the
        #best fit.
        if self.output_ini:
          self.pipeline.create_ini(opt, self.output_ini)

        self.distribution_hints.set_peak(opt, results.post)

        #Also if requested, approximate the covariance matrix with the 
        #inverse of the Hessian matrix.
        #For a gaussian likelihood this is exact.
        covmat = None
        if hasattr(result, 'hess_inv'):
            if self.method == "L-BFGS-B":
                covmat = self.pipeline.denormalize_matrix(result.hess_inv.todense())
            else:
                covmat = self.pipeline.denormalize_matrix(result.hess_inv)
        elif hasattr(result, 'hess'):
            covmat = self.pipeline.denormalize_matrix(np.linalg.inv(result.hess_inv))

        if covmat is None:
            if self.output_cov:
               logs.error("Sorry - the optimization method you chose does not return a covariance (or Hessian) matrix")
        else:
            if self.output_cov:
                np.savetxt(self.output_cov, covmat)
            self.distribution_hints.set_cov(covmat)

        self.converged = True

    def is_converged(self):
        return self.converged
