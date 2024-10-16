with price_range as (
	select 
		advertisement_id,
		count(*) as price_changes,
		min(`datetime`) as initial_date,
		max(`datetime`) as final_date
	from instant_state is2
	group by advertisement_id
)
select 
	adv.id,
	adv.code,
	adv.creation_date,
	adv.last_update_date,
	case WEEKDAY(adv.creation_date)
		when 0 then 'segunda'
		when 1 then 'terça'
		when 2 then 'quarta'
		when 3 then 'quinta'
		when 4 then 'sexta'
		when 5 then 'sábado'
		when 6 then 'domingo'
	end as creation_week_day,
	case WEEKDAY(adv.last_update_date)
		when 0 then 'segunda'
		when 1 then 'terça'
		when 2 then 'quarta'
		when 3 then 'quinta'
		when 4 then 'sexta'
		when 5 then 'sábado'
		when 6 then 'domingo'
	end as last_update_week_day, 
	adv.lat as latitude,
	adv.lon as longitude,
	adv.url,
	adv.city,
	veh.hp,
	veh.gnv,
	veh.`year`,
	case when veh.mileage < 1000 then veh.mileage * 1000 else veh.mileage end as mileage,
	veh.doors,
	#cat.description as category,
	mo.description as model,
	bra.description as brand,
	veh_t.description as vehicle_type,
	fue.description as fuel,
	gea.description as gear,
	col.description as color,
	ste.description as steering,
	first_inst.price as first_price,
	last_inst.price as last_price,
	veh.average_price as olx_average_price,
	veh.fipe_price,
	pri_ran.price_changes,
	group_concat(acc.description order by acc.description asc separator ', ') as accessories
	#(1 - (LEAD(AVG(last_inst.price)) over (partition by mo.description order by mo.description) / AVG(last_inst.price))) * 100 as price_rate_by_model_and_year
from advertisement adv 
left join vehicle veh 
on adv.id = veh.advertisement_id 
left join category cat
on veh.category_id = cat.id 
left join model mo
on veh.model_id = mo.id 
left join brand bra
on veh.brand_id = bra.id
left join vehicle_type veh_t
on veh.vehicle_type_id = veh_t.id
left join fuel fue
on veh.fuel_id = fue.id 
left join gear gea
on veh.gear_id = gea.id
left join color col
on veh.color_id = col.id 
left join steering ste
on veh.steering_id = ste.id
left join price_range pri_ran
on pri_ran.advertisement_id = adv.id
left join instant_state first_inst
on first_inst.advertisement_id = adv.id 
and first_inst.`datetime` = pri_ran.initial_date
left join instant_state last_inst
on last_inst.advertisement_id = adv.id 
and last_inst.`datetime` = pri_ran.final_date
left join vehicle_accessory veh_acc
on veh_acc.vehicle_id = veh.id 
left join accessory acc
on veh_acc.accessory_id = acc.id
group by adv.id
order by adv.creation_date;