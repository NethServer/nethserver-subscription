<?php
namespace NethServer\Module;

/*
 * Copyright (C) 2017 Nethesis S.r.l.
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

use Nethgui\System\PlatformInterface as Validate;

/**
 * Manage and display alerts
 *
 */
class Alerts extends \Nethgui\Controller\TableController
{

    protected function initializeAttributes(\Nethgui\Module\ModuleAttributesInterface $attributes)
    {
        // currently this module is available only for Enterprise subscriptions
        if (@file_exists("/etc/e-smith/db/configuration/defaults/nethupdate/type")) {
            return new \NethServer\Tool\CustomModuleAttributesProvider($attributes, array(
                'category' => 'Management')
            );
        } else {
            return new \NethServer\Tool\CustomModuleAttributesProvider($attributes);
        }
    }

    public function initialize()
    {
        $columns = array(
            'Type',
            'Instance',
            'Threshold'
        );

        $this
            ->setTableAdapter(new \Nethgui\Adapter\LazyLoaderAdapter(array($this, 'readAlerts')))
            ->setColumns($columns)
            ->addTableAction(new Alerts\Refresh())
            ->addTableAction(new Alerts\Configure())
        ;

        parent::initialize();
    }

    public function readAlerts()
    {
        $loader = new \ArrayObject();
        $alarms = $this->getPlatform()->getDatabase('alerts')->getAll();
        foreach($alarms as $alarm => $props) {
            $loader[$alarm] = array(
                'Type' => $props['type'],
                'PluginType' => $props['PluginType'],
                'Instance' => $props['Instance'],
                'FailureMin' => $props['FailureMin'],
                'FailureMax' => $props['FailureMax'],
                'WarningMax' => $props['WarningMax'],
                'WarningMin' => $props['WarningMin']
            );
        }
        return $loader;
    }

    public function prepareViewForColumnInstance(\Nethgui\Controller\Table\Read $action, \Nethgui\View\ViewInterface $view, $key, $values, &$rowMetadata)
    {
        switch ($values['Type']) {
            case "df":
               return $view->translate("Partition_label").": /".$values['Instance'];
            case "swap":
               return '-';
            case "ping":
               return $view->translate("Host_label").": ".$values['Instance'];
            default:
               return $values['Instance'] ? $values['Instance'] : '-';
        }
    }

    public function prepareViewForColumnThreshold(\Nethgui\Controller\Table\Read $action, \Nethgui\View\ViewInterface $view, $key, $values, &$rowMetadata)
    {
        switch ($values['Type']) {
            case 'load':
                 return $view->translate("max_fail_label").": ".$values['FailureMax'].", ".$view->translate("max_warn_label").": ".$values['WarningMax'];
            case "df":
            case "swap":
               return  $view->translate("min_fail_label").": ".$values['FailureMin']." %";
            case "ping":
                if($values['PluginType'] == 'ping_droprate') {
                    return $view->translate("max_fail_label").": " . ( $values['FailureMax'] * 100 ) . " %";
                } else {
                    return $view->translate("max_fail_label").": ".$values['FailureMax'] . " ms";
                }
            default:
               return '-';
        }
    }


    public function prepareViewForColumnType(\Nethgui\Controller\Table\Read $action, \Nethgui\View\ViewInterface $view, $key, $values, &$rowMetadata)
    {
        if($values['Type'] == 'ping') {
            return $view->translate($values['PluginType']."_label");
        }
        return $view->translate($values['Type']."_label");
    }

    # HACK: change table view (thanks to DavideP)
    public function prepareView(\Nethgui\View\ViewInterface $view)
    {
        parent::prepareView($view);
        if (isset($view['read'])) {
            $url_parts = parse_url($this->getPlatform()->getDatabase('configuration')->getProp('subscription', 'AlertsUrl'));
            $view['read']['Url'] = $url_parts['scheme']."://".$url_parts['host'];

            $view['read']->setTemplate('NethServer\Template\Alerts');
            $view['read']['updated'] = '-';
            if ( file_exists('/var/lib/nethserver/db/alerts') ) {
                $stats = stat('/var/lib/nethserver/db/alerts');
                $view['read']['updated'] = date("D M j G:i:s T Y",$stats[9]);
            }
        }
    }
}
