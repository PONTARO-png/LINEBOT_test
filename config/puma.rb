
# config/puma.rb

 before_fork do
   require 'puma_worker_killer'
 
   PumaWorkerKiller.enable_rolling_restart # Default is every 6 hours
 end
 # config/puma.rb

before_fork do
  require 'puma_worker_killer'

  PumaWorkerKiller.start
end