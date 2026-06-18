import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { ChargingDetailComponent } from './charging-detail/charging-detail.component';
import { ChargingListComponent } from './charging-list/charging-list.component';
import { ChargingRecordListComponent } from './charging-record-list/charging-record-list.component';

@NgModule({
  declarations: [ChargingListComponent, ChargingDetailComponent, ChargingRecordListComponent],
  imports: [SharedModule, RouterModule.forChild([
    { path: '', component: ChargingListComponent },
    { path: 'records', component: ChargingRecordListComponent },
    { path: ':id', component: ChargingDetailComponent }
  ])]
})
export class ChargingModule {}
