<?php

/*
 * Copyright (C) 2018 Nethesis S.r.l.
 * 
 * This script is part of NethServer.
 * 
 * NethServer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * NethServer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with NethServer.  If not, see <http://www.gnu.org/licenses/>.
 */

namespace NethServer\Module\Subscription;


class Properties extends \Nethgui\Controller\AbstractController implements \Nethgui\Component\DependencyConsumer
{
    public function initialize()
    {
        parent::initialize();
        $this->declareParameter('SystemId', FALSE, array('configuration', 'subscription', 'SystemId'));
    }

    public function prepareView(\Nethgui\View\ViewInterface $view)
    {
        parent::prepareView($view);

        $secret = $this->getPlatform()->getDatabase('configuration')->getProp('subscription','Secret');
        if($secret) {
            $plan = $this->getParent()->readSubscriptionPlan($secret);
            if (isset($plan['created'])) {
                $created = new \DateTime($plan['created']);
                $view['Created'] = $created->format('Y-m-d');
            }
            if (isset($plan['subscription']['valid_from']) && isset($plan['subscription']['valid_until'])) {
                $from = new \DateTime($plan['subscription']['valid_from']);
                $until = new \DateTime($plan['subscription']['valid_until']);
                $view['Validity'] = $from->format('Y-m-d') . " - " . $until->format('Y-m-d');
            }
            if (isset($plan['subscription']['subscription_plan']['name'])) {
                $view['PlanName'] = $plan['subscription']['subscription_plan']['name'];
            }
            if (isset($plan['public_ip'])) {
                $view['PublicIp'] = $plan['public_ip'];
            }
        }
        
        if($this->getRequest()->hasParameter('registerSuccess')) {
            $this->notifications->message($view->translate('registerSuccess_notification'));
            $view->getCommandList()->show();
        }
    }
    
    public function setUserNotifications(\Nethgui\Model\UserNotifications $n)
    {
        $this->notifications = $n;
        return $this;
    }

    public function getDependencySetters()
    {
        return array(
            'UserNotifications' => array($this, 'setUserNotifications'),
        );
    }
}
